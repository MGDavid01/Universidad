from django.db import transaction
from django.utils import timezone

from .models import Quote, ScopeChange, ServiceRequest


class ServiceFlowError(Exception):
    """Error de reglas de negocio del flujo de servicio."""


@transaction.atomic
def accept_quote(*, service_request: ServiceRequest, quote: Quote, actor):
    if actor.organization_id != service_request.client_id:
        raise ServiceFlowError("Solo el cliente dueño puede aceptar cotizaciones.")
    if quote.service_request_id != service_request.id:
        raise ServiceFlowError("La cotización no pertenece a esta solicitud.")
    if service_request.status not in {
        ServiceRequest.Status.OPEN,
        ServiceRequest.Status.QUOTED,
    }:
        raise ServiceFlowError("La solicitud ya no admite aceptación de cotizaciones.")
    if quote.status != Quote.Status.PENDING:
        raise ServiceFlowError("Solo se pueden aceptar cotizaciones pendientes.")

    service_request.quotes.exclude(pk=quote.pk).filter(status=Quote.Status.PENDING).update(
        status=Quote.Status.REJECTED
    )
    quote.status = Quote.Status.ACCEPTED
    quote.save(update_fields=["status", "updated_at"])

    service_request.selected_quote = quote
    service_request.selected_provider = quote.provider
    service_request.status = ServiceRequest.Status.ACCEPTED
    service_request.save(
        update_fields=[
            "selected_quote",
            "selected_provider",
            "status",
            "updated_at",
        ]
    )
    return service_request


@transaction.atomic
def mark_on_site(*, service_request: ServiceRequest, actor):
    if actor.organization_id != service_request.selected_provider_id:
        raise ServiceFlowError("Solo el proveedor asignado puede marcar en sitio.")
    if service_request.status != ServiceRequest.Status.ACCEPTED:
        raise ServiceFlowError("La solicitud debe estar aceptada para marcar en sitio.")
    service_request.status = ServiceRequest.Status.ON_SITE
    service_request.save(update_fields=["status", "updated_at"])
    return service_request


@transaction.atomic
def create_scope_change(*, service_request: ServiceRequest, quote: Quote, actor, cleaned_data):
    if actor.organization_id != service_request.selected_provider_id:
        raise ServiceFlowError("Solo el proveedor asignado puede registrar un cambio de alcance.")
    if service_request.status not in {
        ServiceRequest.Status.ACCEPTED,
        ServiceRequest.Status.ON_SITE,
    }:
        raise ServiceFlowError("No se puede solicitar cambio de alcance en este estado.")
    if quote.id != service_request.selected_quote_id:
        raise ServiceFlowError("El cambio debe referirse a la cotización aceptada.")
    if service_request.scope_changes.filter(status=ScopeChange.Status.PENDING).exists():
        raise ServiceFlowError("Ya existe un cambio de alcance pendiente.")

    change = ScopeChange.objects.create(
        service_request=service_request,
        quote=quote,
        created_by=actor,
        **cleaned_data,
    )
    service_request.status = ServiceRequest.Status.SCOPE_CHANGE
    service_request.save(update_fields=["status", "updated_at"])
    return change


@transaction.atomic
def decide_scope_change(*, change: ScopeChange, actor, approve: bool):
    service_request = change.service_request
    if actor.organization_id != service_request.client_id:
        raise ServiceFlowError("Solo el cliente dueño puede decidir el cambio de alcance.")
    if change.status != ScopeChange.Status.PENDING:
        raise ServiceFlowError("Este cambio de alcance ya fue resuelto.")

    change.status = ScopeChange.Status.APPROVED if approve else ScopeChange.Status.REJECTED
    change.decided_at = timezone.now()
    change.save(update_fields=["status", "decided_at"])

    if approve:
        quote = change.quote
        quote.scope = change.new_scope
        quote.amount = change.revised_amount
        quote.save(update_fields=["scope", "amount", "updated_at"])
        service_request.status = ServiceRequest.Status.ON_SITE
    else:
        service_request.status = ServiceRequest.Status.ON_SITE
    service_request.save(update_fields=["status", "updated_at"])
    return change


@transaction.atomic
def complete_request(*, service_request: ServiceRequest, actor):
    allowed_orgs = {service_request.client_id, service_request.selected_provider_id}
    if actor.organization_id not in allowed_orgs:
        raise ServiceFlowError("No tienes permiso para finalizar esta solicitud.")
    if service_request.status not in {
        ServiceRequest.Status.ACCEPTED,
        ServiceRequest.Status.ON_SITE,
    }:
        raise ServiceFlowError("La solicitud no puede finalizarse en este estado.")
    if service_request.scope_changes.filter(status=ScopeChange.Status.PENDING).exists():
        raise ServiceFlowError("Hay un cambio de alcance pendiente de aprobación.")
    service_request.status = ServiceRequest.Status.COMPLETED
    service_request.save(update_fields=["status", "updated_at"])
    return service_request
