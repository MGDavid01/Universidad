from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction

from .models import (
    Organization,
    ProviderProfile,
    Quote,
    Review,
    ScopeChange,
    ServiceRequest,
    User,
)


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                continue
            if isinstance(field.widget, forms.CheckboxInput):
                continue
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{css} form-control".strip()


class LoginForm(StyledFormMixin, AuthenticationForm):
    pass


class RegisterForm(StyledFormMixin, forms.Form):
    username = forms.CharField(label="Usuario", max_length=150)
    email = forms.EmailField(label="Correo")
    first_name = forms.CharField(label="Nombre", max_length=150)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)
    organization_name = forms.CharField(label="Nombre de la empresa", max_length=200)
    phone = forms.CharField(label="Teléfono", max_length=40, required=False)
    zone = forms.CharField(label="Zona", max_length=100)
    role = forms.ChoiceField(
        label="Tipo de cuenta",
        choices=User.Role.choices,
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este usuario ya existe.")
        return username

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned

    @transaction.atomic
    def save(self):
        role = self.cleaned_data["role"]
        org_type = (
            Organization.OrgType.PROVIDER
            if role == User.Role.PROVIDER
            else Organization.OrgType.CLIENT
        )
        organization = Organization.objects.create(
            name=self.cleaned_data["organization_name"],
            org_type=org_type,
            contact_email=self.cleaned_data["email"],
            phone=self.cleaned_data.get("phone", ""),
            zone=self.cleaned_data["zone"],
        )
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            password=self.cleaned_data["password1"],
            role=role,
            organization=organization,
        )
        if role == User.Role.PROVIDER:
            ProviderProfile.objects.create(
                organization=organization,
                coverage_zone=self.cleaned_data["zone"],
                description="",
            )
        return user


class ProviderProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = ProviderProfile
        fields = ("description", "coverage_zone", "is_available", "specialties")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "specialties": forms.CheckboxSelectMultiple,
        }


class ServiceRequestForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ("title", "category", "urgency", "location", "description")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class QuoteForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Quote
        fields = ("scope", "amount", "estimated_time")
        widgets = {
            "scope": forms.Textarea(attrs={"rows": 4}),
        }


class ScopeChangeForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = ScopeChange
        fields = ("finding", "new_scope", "revised_amount", "evidence_notes")
        widgets = {
            "finding": forms.Textarea(attrs={"rows": 3}),
            "new_scope": forms.Textarea(attrs={"rows": 3}),
            "evidence_notes": forms.Textarea(attrs={"rows": 2}),
        }


class ReviewForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "comment")
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 3}),
        }
