from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg


class Organization(models.Model):
    class OrgType(models.TextChoices):
        CLIENT = "cliente", "Empresa cliente"
        PROVIDER = "proveedor", "Pyme proveedora"

    name = models.CharField("nombre", max_length=200)
    org_type = models.CharField("tipo", max_length=20, choices=OrgType.choices)
    contact_email = models.EmailField("correo de contacto")
    phone = models.CharField("teléfono", max_length=40, blank=True)
    zone = models.CharField("zona", max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "organización"
        verbose_name_plural = "organizaciones"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_org_type_display()})"


class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = "cliente", "Cliente"
        PROVIDER = "proveedor", "Proveedor"

    role = models.CharField("rol", max_length=20, choices=Role.choices)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="users",
        verbose_name="organización",
    )

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    def __str__(self):
        return f"{self.username} · {self.get_role_display()}"

    @property
    def is_client(self):
        return self.role == self.Role.CLIENT

    @property
    def is_provider(self):
        return self.role == self.Role.PROVIDER


class Category(models.Model):
    name = models.CharField("nombre", max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField("descripción", blank=True)

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ProviderProfile(models.Model):
    organization = models.OneToOneField(
        Organization,
        on_delete=models.CASCADE,
        related_name="provider_profile",
        limit_choices_to={"org_type": Organization.OrgType.PROVIDER},
    )
    specialties = models.ManyToManyField(Category, related_name="providers", blank=True)
    description = models.TextField("descripción", blank=True)
    coverage_zone = models.CharField("zona de cobertura", max_length=100, blank=True)
    is_available = models.BooleanField("disponible", default=True)
    average_rating = models.DecimalField(
        "calificación promedio",
        max_digits=3,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    review_count = models.PositiveIntegerField("número de reseñas", default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "perfil de proveedor"
        verbose_name_plural = "perfiles de proveedor"

    def __str__(self):
        return self.organization.name

    def refresh_rating(self):
        reviews = Review.objects.filter(
            service_request__selected_provider=self.organization,
            service_request__status=ServiceRequest.Status.COMPLETED,
        )
        agg = reviews.aggregate(avg=Avg("rating"), count=models.Count("id"))
        self.average_rating = Decimal(str(round(agg["avg"] or 0, 2)))
        self.review_count = agg["count"] or 0
        self.save(update_fields=["average_rating", "review_count", "updated_at"])


class ServiceRequest(models.Model):
    class Urgency(models.TextChoices):
        NORMAL = "normal", "Normal (24–48 h)"
        HIGH = "alta", "Alta (hoy)"
        CRITICAL = "critica", "Crítica (ahora)"

    class Status(models.TextChoices):
        OPEN = "abierta", "Abierta"
        QUOTED = "cotizada", "Con cotizaciones"
        ACCEPTED = "aceptada", "Cotización aceptada"
        ON_SITE = "en_sitio", "En sitio"
        SCOPE_CHANGE = "cambio_alcance", "Cambio de alcance"
        COMPLETED = "finalizada", "Finalizada"
        CANCELLED = "cancelada", "Cancelada"

    client = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="service_requests",
        limit_choices_to={"org_type": Organization.OrgType.CLIENT},
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_requests",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="service_requests",
    )
    title = models.CharField("título", max_length=200)
    description = models.TextField("descripción")
    urgency = models.CharField(
        "urgencia",
        max_length=20,
        choices=Urgency.choices,
        default=Urgency.NORMAL,
    )
    location = models.CharField("ubicación", max_length=200)
    status = models.CharField(
        "estado",
        max_length=30,
        choices=Status.choices,
        default=Status.OPEN,
    )
    selected_provider = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="accepted_requests",
        limit_choices_to={"org_type": Organization.OrgType.PROVIDER},
    )
    selected_quote = models.ForeignKey(
        "Quote",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "solicitud de servicio"
        verbose_name_plural = "solicitudes de servicio"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} · {self.get_status_display()}"


class Quote(models.Model):
    class Status(models.TextChoices):
        PENDING = "pendiente", "Pendiente"
        ACCEPTED = "aceptada", "Aceptada"
        REJECTED = "rechazada", "Rechazada"
        SUPERSEDED = "reemplazada", "Reemplazada"

    service_request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name="quotes",
    )
    provider = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="quotes",
        limit_choices_to={"org_type": Organization.OrgType.PROVIDER},
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="quotes",
    )
    scope = models.TextField("alcance")
    amount = models.DecimalField(
        "importe estimado",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    estimated_time = models.CharField("tiempo estimado", max_length=100)
    status = models.CharField(
        "estado",
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "cotización"
        verbose_name_plural = "cotizaciones"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["service_request", "provider"],
                name="unique_quote_per_provider_request",
            )
        ]

    def __str__(self):
        return f"{self.provider.name} · ${self.amount} · {self.get_status_display()}"


class ScopeChange(models.Model):
    class Status(models.TextChoices):
        PENDING = "pendiente", "Pendiente de aprobación"
        APPROVED = "aprobado", "Aprobado"
        REJECTED = "rechazado", "Rechazado"

    service_request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name="scope_changes",
    )
    quote = models.ForeignKey(
        Quote,
        on_delete=models.CASCADE,
        related_name="scope_changes",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="scope_changes",
    )
    finding = models.TextField("hallazgo en sitio")
    new_scope = models.TextField("nuevo alcance")
    revised_amount = models.DecimalField(
        "monto revisado",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    evidence_notes = models.TextField("evidencias / notas", blank=True)
    status = models.CharField(
        "estado",
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    decided_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "cambio de alcance"
        verbose_name_plural = "cambios de alcance"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Cambio · {self.service_request.title} · {self.get_status_display()}"


class Review(models.Model):
    service_request = models.OneToOneField(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name="review",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="reviews",
    )
    rating = models.PositiveSmallIntegerField(
        "calificación",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.TextField("comentario", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "reseña"
        verbose_name_plural = "reseñas"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.rating}/5 · {self.service_request.title}"
