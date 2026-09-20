from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from .decorators import role_required
from .forms import (
    LoginForm,
    ProviderProfileForm,
    QuoteForm,
    RegisterForm,
    ReviewForm,
    ScopeChangeForm,
    ServiceRequestForm,
)
from .models import (
    Category,
    ProviderProfile,
    Quote,
    Review,
    ScopeChange,
    ServiceRequest,
)
from .services import (
    ServiceFlowError,
    accept_quote,
    complete_request,
    create_scope_change,
    decide_scope_change,
    mark_on_site,
)


class AppLoginView(LoginView):
    template_name = "core/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class AppLogoutView(LogoutView):
    next_page = reverse_lazy("home")


def home(request):
    providers = (
        ProviderProfile.objects.select_related("organization")
        .prefetch_related("specialties")
        .filter(is_available=True)[:6]
    )
    return render(request, "core/home.html", {"providers": providers})


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Cuenta creada correctamente.")
        return redirect("dashboard")
    return render(request, "core/register.html", {"form": form})


@login_required
def dashboard(request):
    user = request.user
    if user.is_client:
        requests_qs = (
            ServiceRequest.objects.filter(client=user.organization)
            .select_related("category", "selected_provider")
            .prefetch_related("quotes")
        )
        return render(
            request,
            "core/dashboard_client.html",
            {"requests": requests_qs},
        )

    profile = getattr(user.organization, "provider_profile", None)
    specialty_ids = []
    if profile:
        specialty_ids = list(profile.specialties.values_list("id", flat=True))

    opportunities = (
        ServiceRequest.objects.filter(
            status__in=[ServiceRequest.Status.OPEN, ServiceRequest.Status.QUOTED],
        )
        .filter(Q(category_id__in=specialty_ids) | Q(category_id__isnull=False))
        .exclude(quotes__provider=user.organization)
        .select_related("category", "client")
        .distinct()
    )
    if specialty_ids:
        opportunities = opportunities.filter(category_id__in=specialty_ids)

    my_jobs = (
        ServiceRequest.objects.filter(selected_provider=user.organization)
        .exclude(status=ServiceRequest.Status.COMPLETED)
        .select_related("category", "client", "selected_quote")
    )
    my_quotes = (
        Quote.objects.filter(provider=user.organization)
        .select_related("service_request")
        .order_by("-created_at")[:10]
    )
    return render(
        request,
        "core/dashboard_provider.html",
        {
            "profile": profile,
            "opportunities": opportunities[:20],
            "my_jobs": my_jobs,
            "my_quotes": my_quotes,
        },
    )


def provider_directory(request):
    category_slug = request.GET.get("categoria")
    zone = request.GET.get("zona", "").strip()
    providers = (
        ProviderProfile.objects.select_related("organization")
        .prefetch_related("specialties")
        .filter(is_available=True)
    )
    if category_slug:
        providers = providers.filter(specialties__slug=category_slug)
    if zone:
        providers = providers.filter(coverage_zone__icontains=zone)
    categories = Category.objects.all()
    return render(
        request,
        "core/directory.html",
        {
            "providers": providers.distinct(),
            "categories": categories,
            "selected_category": category_slug or "",
            "selected_zone": zone,
        },
    )


@login_required
@role_required("proveedor")
def provider_profile_edit(request):
    profile, _ = ProviderProfile.objects.get_or_create(
        organization=request.user.organization,
        defaults={"coverage_zone": request.user.organization.zone},
    )
    form = ProviderProfileForm(request.POST or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Perfil de proveedor actualizado.")
        return redirect("dashboard")
    return render(request, "core/provider_profile_form.html", {"form": form})


@login_required
@role_required("cliente")
def request_create(request):
    initial = {}
    provider_id = request.GET.get("proveedor")
    category_id = request.GET.get("categoria")
    if category_id:
        initial["category"] = category_id
    form = ServiceRequestForm(request.POST or None, initial=initial)
    preferred_provider = None
    if provider_id:
        preferred_provider = ProviderProfile.objects.filter(
            organization_id=provider_id
        ).select_related("organization").first()
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.client = request.user.organization
        obj.created_by = request.user
        obj.save()
        messages.success(request, "Solicitud creada. Los proveedores compatibles podrán cotizar.")
        return redirect("request_detail", pk=obj.pk)
    return render(
        request,
        "core/request_form.html",
        {"form": form, "preferred_provider": preferred_provider},
    )


@login_required
def request_detail(request, pk):
    service_request = get_object_or_404(
        ServiceRequest.objects.select_related(
            "category", "client", "selected_provider", "selected_quote"
        ).prefetch_related("quotes__provider", "scope_changes"),
        pk=pk,
    )
    user = request.user
    is_owner = user.organization_id == service_request.client_id
    is_selected = user.organization_id == service_request.selected_provider_id
    is_provider = user.is_provider

    if not (is_owner or is_selected or is_provider):
        messages.error(request, "No tienes acceso a esta solicitud.")
        return redirect("dashboard")

    # Proveedores solo ven solicitudes abiertas/compatibles o las suyas
    if is_provider and not is_selected and not is_owner:
        if service_request.status not in {
            ServiceRequest.Status.OPEN,
            ServiceRequest.Status.QUOTED,
        }:
            messages.error(request, "Esta solicitud ya no está disponible.")
            return redirect("dashboard")

    quote_form = None
    scope_form = None
    review_form = None
    existing_quote = None
    pending_change = service_request.scope_changes.filter(
        status=ScopeChange.Status.PENDING
    ).first()

    if is_provider and not is_selected and service_request.status in {
        ServiceRequest.Status.OPEN,
        ServiceRequest.Status.QUOTED,
    }:
        existing_quote = service_request.quotes.filter(
            provider=user.organization
        ).first()
        if not existing_quote:
            quote_form = QuoteForm()

    if is_selected and service_request.status in {
        ServiceRequest.Status.ACCEPTED,
        ServiceRequest.Status.ON_SITE,
    }:
        if not pending_change:
            scope_form = ScopeChangeForm()

    if (
        is_owner
        and service_request.status == ServiceRequest.Status.COMPLETED
        and not hasattr(service_request, "review")
    ):
        review_form = ReviewForm()

    return render(
        request,
        "core/request_detail.html",
        {
            "service_request": service_request,
            "is_owner": is_owner,
            "is_selected": is_selected,
            "quote_form": quote_form,
            "existing_quote": existing_quote,
            "scope_form": scope_form,
            "pending_change": pending_change,
            "review_form": review_form,
        },
    )


@login_required
@role_required("proveedor")
@require_POST
def quote_create(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    if service_request.status not in {
        ServiceRequest.Status.OPEN,
        ServiceRequest.Status.QUOTED,
    }:
        messages.error(request, "Esta solicitud ya no admite cotizaciones.")
        return redirect("request_detail", pk=pk)
    if service_request.quotes.filter(provider=request.user.organization).exists():
        messages.error(request, "Ya enviaste una cotización para esta solicitud.")
        return redirect("request_detail", pk=pk)

    form = QuoteForm(request.POST)
    if form.is_valid():
        quote = form.save(commit=False)
        quote.service_request = service_request
        quote.provider = request.user.organization
        quote.created_by = request.user
        quote.save()
        if service_request.status == ServiceRequest.Status.OPEN:
            service_request.status = ServiceRequest.Status.QUOTED
            service_request.save(update_fields=["status", "updated_at"])
        messages.success(request, "Cotización enviada.")
    else:
        messages.error(request, "Revisa los datos de la cotización.")
    return redirect("request_detail", pk=pk)


@login_required
@role_required("cliente")
@require_POST
def quote_accept(request, pk, quote_id):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    quote = get_object_or_404(Quote, pk=quote_id, service_request=service_request)
    try:
        accept_quote(service_request=service_request, quote=quote, actor=request.user)
        messages.success(request, f"Cotización de {quote.provider.name} aceptada.")
    except ServiceFlowError as exc:
        messages.error(request, str(exc))
    return redirect("request_detail", pk=pk)


@login_required
@role_required("proveedor")
@require_POST
def request_mark_on_site(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    try:
        mark_on_site(service_request=service_request, actor=request.user)
        messages.success(request, "Estado actualizado a «En sitio».")
    except ServiceFlowError as exc:
        messages.error(request, str(exc))
    return redirect("request_detail", pk=pk)


@login_required
@role_required("proveedor")
@require_POST
def scope_change_create(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    quote = service_request.selected_quote
    if not quote:
        messages.error(request, "No hay cotización aceptada.")
        return redirect("request_detail", pk=pk)
    form = ScopeChangeForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Revisa los datos del cambio de alcance.")
        return redirect("request_detail", pk=pk)
    try:
        create_scope_change(
            service_request=service_request,
            quote=quote,
            actor=request.user,
            cleaned_data=form.cleaned_data,
        )
        messages.success(
            request,
            "Cambio de alcance enviado. El cliente debe aprobarlo antes de continuar.",
        )
    except ServiceFlowError as exc:
        messages.error(request, str(exc))
    return redirect("request_detail", pk=pk)


@login_required
@role_required("cliente")
@require_POST
def scope_change_decide(request, pk, change_id):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    change = get_object_or_404(
        ScopeChange, pk=change_id, service_request=service_request
    )
    approve = request.POST.get("decision") == "approve"
    try:
        decide_scope_change(change=change, actor=request.user, approve=approve)
        if approve:
            messages.success(request, "Cambio de alcance aprobado. La cotización se actualizó.")
        else:
            messages.info(
                request,
                "Cambio de alcance rechazado. El trabajo continúa con el alcance original o se cierra.",
            )
    except ServiceFlowError as exc:
        messages.error(request, str(exc))
    return redirect("request_detail", pk=pk)


@login_required
@require_POST
def request_complete(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    try:
        complete_request(service_request=service_request, actor=request.user)
        messages.success(request, "Solicitud marcada como finalizada.")
    except ServiceFlowError as exc:
        messages.error(request, str(exc))
    return redirect("request_detail", pk=pk)


@login_required
@role_required("cliente")
@require_POST
def review_create(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    if service_request.client_id != request.user.organization_id:
        messages.error(request, "Solo el cliente puede calificar.")
        return redirect("request_detail", pk=pk)
    if service_request.status != ServiceRequest.Status.COMPLETED:
        messages.error(request, "Solo se califican solicitudes finalizadas.")
        return redirect("request_detail", pk=pk)
    if hasattr(service_request, "review"):
        messages.error(request, "Esta solicitud ya tiene una reseña.")
        return redirect("request_detail", pk=pk)

    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.service_request = service_request
        review.author = request.user
        review.save()
        if service_request.selected_provider:
            profile = getattr(service_request.selected_provider, "provider_profile", None)
            if profile:
                profile.refresh_rating()
        messages.success(request, "Gracias por tu calificación.")
    else:
        messages.error(request, "Revisa la calificación.")
    return redirect("request_detail", pk=pk)
