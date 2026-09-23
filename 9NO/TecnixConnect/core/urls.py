from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("registro/", views.register, name="register"),
    path("entrar/", views.AppLoginView.as_view(), name="login"),
    path("salir/", views.AppLogoutView.as_view(), name="logout"),
    path("panel/", views.dashboard, name="dashboard"),
    path("proveedores/", views.provider_directory, name="directory"),
    path("proveedor/perfil/", views.provider_profile_edit, name="provider_profile"),
    path("solicitudes/nueva/", views.request_create, name="request_create"),
    path("solicitudes/<int:pk>/", views.request_detail, name="request_detail"),
    path("solicitudes/<int:pk>/cotizar/", views.quote_create, name="quote_create"),
    path(
        "solicitudes/<int:pk>/cotizaciones/<int:quote_id>/aceptar/",
        views.quote_accept,
        name="quote_accept",
    ),
    path(
        "solicitudes/<int:pk>/en-sitio/",
        views.request_mark_on_site,
        name="request_on_site",
    ),
    path(
        "solicitudes/<int:pk>/cambio-alcance/",
        views.scope_change_create,
        name="scope_change_create",
    ),
    path(
        "solicitudes/<int:pk>/cambio-alcance/<int:change_id>/decidir/",
        views.scope_change_decide,
        name="scope_change_decide",
    ),
    path(
        "solicitudes/<int:pk>/finalizar/",
        views.request_complete,
        name="request_complete",
    ),
    path(
        "solicitudes/<int:pk>/reseña/",
        views.review_create,
        name="review_create",
    ),
]
