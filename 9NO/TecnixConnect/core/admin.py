from django.contrib import admin

from .models import (
    Category,
    Organization,
    ProviderProfile,
    Quote,
    Review,
    ScopeChange,
    ServiceRequest,
    User,
)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "org_type", "zone", "contact_email", "created_at")
    list_filter = ("org_type", "zone")
    search_fields = ("name", "contact_email")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "organization", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


class SpecialtyInline(admin.TabularInline):
    model = ProviderProfile.specialties.through
    extra = 1


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "coverage_zone",
        "is_available",
        "average_rating",
        "review_count",
    )
    list_filter = ("is_available", "coverage_zone")
    search_fields = ("organization__name",)
    filter_horizontal = ("specialties",)


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "client",
        "category",
        "urgency",
        "status",
        "selected_provider",
        "created_at",
    )
    list_filter = ("status", "urgency", "category")
    search_fields = ("title", "description", "client__name")


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = (
        "service_request",
        "provider",
        "amount",
        "status",
        "estimated_time",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = ("provider__name", "service_request__title")


@admin.register(ScopeChange)
class ScopeChangeAdmin(admin.ModelAdmin):
    list_display = (
        "service_request",
        "revised_amount",
        "status",
        "created_at",
        "decided_at",
    )
    list_filter = ("status",)
    search_fields = ("service_request__title", "finding")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("service_request", "rating", "author", "created_at")
    list_filter = ("rating",)
