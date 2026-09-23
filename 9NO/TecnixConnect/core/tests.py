from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from core.models import (
    Category,
    Organization,
    ProviderProfile,
    Quote,
    ScopeChange,
    ServiceRequest,
)
from core.services import (
    ServiceFlowError,
    accept_quote,
    create_scope_change,
    decide_scope_change,
)

User = get_user_model()


class BaseFlowTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Hardware / PCs",
            slug="hardware",
            description="Equipos",
        )
        self.client_org = Organization.objects.create(
            name="Comercio Norte",
            org_type=Organization.OrgType.CLIENT,
            contact_email="cliente@example.com",
            zone="Norte",
        )
        self.provider_org = Organization.objects.create(
            name="PC Doctor",
            org_type=Organization.OrgType.PROVIDER,
            contact_email="prov@example.com",
            zone="Norte",
        )
        self.other_provider = Organization.objects.create(
            name="Otro Tech",
            org_type=Organization.OrgType.PROVIDER,
            contact_email="otro@example.com",
            zone="Sur",
        )
        self.client_user = User.objects.create_user(
            username="cliente1",
            password="pass12345",
            role=User.Role.CLIENT,
            organization=self.client_org,
            email="cliente@example.com",
        )
        self.provider_user = User.objects.create_user(
            username="prov1",
            password="pass12345",
            role=User.Role.PROVIDER,
            organization=self.provider_org,
            email="prov@example.com",
        )
        self.other_provider_user = User.objects.create_user(
            username="prov2",
            password="pass12345",
            role=User.Role.PROVIDER,
            organization=self.other_provider,
            email="otro@example.com",
        )
        profile = ProviderProfile.objects.create(
            organization=self.provider_org,
            coverage_zone="Norte",
            description="Soporte hardware",
        )
        profile.specialties.add(self.category)
        ProviderProfile.objects.create(
            organization=self.other_provider,
            coverage_zone="Sur",
        )
        self.service_request = ServiceRequest.objects.create(
            client=self.client_org,
            created_by=self.client_user,
            category=self.category,
            title="PC no enciende",
            description="Sospecha de PSU dañada",
            urgency=ServiceRequest.Urgency.HIGH,
            location="Norte",
        )


class ServiceFlowTests(BaseFlowTestCase):
    def test_full_cycle_with_scope_change_approval(self):
        quote = Quote.objects.create(
            service_request=self.service_request,
            provider=self.provider_org,
            created_by=self.provider_user,
            scope="Cambio de PSU",
            amount=Decimal("100.00"),
            estimated_time="mismo día",
        )
        self.service_request.status = ServiceRequest.Status.QUOTED
        self.service_request.save()

        accept_quote(
            service_request=self.service_request,
            quote=quote,
            actor=self.client_user,
        )
        self.service_request.refresh_from_db()
        self.assertEqual(self.service_request.status, ServiceRequest.Status.ACCEPTED)
        self.assertEqual(self.service_request.selected_provider, self.provider_org)

        change = create_scope_change(
            service_request=self.service_request,
            quote=quote,
            actor=self.provider_user,
            cleaned_data={
                "finding": "También falla la Motherboard",
                "new_scope": "Cambio de PSU + Motherboard",
                "revised_amount": Decimal("1850.00"),
                "evidence_notes": "Fotos del diagnóstico",
            },
        )
        self.service_request.refresh_from_db()
        self.assertEqual(self.service_request.status, ServiceRequest.Status.SCOPE_CHANGE)
        self.assertEqual(change.status, ScopeChange.Status.PENDING)

        decide_scope_change(change=change, actor=self.client_user, approve=True)
        quote.refresh_from_db()
        self.service_request.refresh_from_db()
        self.assertEqual(quote.amount, Decimal("1850.00"))
        self.assertIn("Motherboard", quote.scope)
        self.assertEqual(self.service_request.status, ServiceRequest.Status.ON_SITE)

    def test_foreign_client_cannot_accept_quote(self):
        other_client_org = Organization.objects.create(
            name="Otro Cliente",
            org_type=Organization.OrgType.CLIENT,
            contact_email="x@example.com",
            zone="Centro",
        )
        other_client = User.objects.create_user(
            username="cliente2",
            password="pass12345",
            role=User.Role.CLIENT,
            organization=other_client_org,
        )
        quote = Quote.objects.create(
            service_request=self.service_request,
            provider=self.provider_org,
            created_by=self.provider_user,
            scope="Cambio de PSU",
            amount=Decimal("100.00"),
            estimated_time="1 día",
        )
        with self.assertRaises(ServiceFlowError):
            accept_quote(
                service_request=self.service_request,
                quote=quote,
                actor=other_client,
            )

    def test_scope_change_reject_keeps_original_amount(self):
        quote = Quote.objects.create(
            service_request=self.service_request,
            provider=self.provider_org,
            created_by=self.provider_user,
            scope="Cambio de PSU",
            amount=Decimal("100.00"),
            estimated_time="mismo día",
        )
        accept_quote(
            service_request=self.service_request,
            quote=quote,
            actor=self.client_user,
        )
        change = create_scope_change(
            service_request=self.service_request,
            quote=quote,
            actor=self.provider_user,
            cleaned_data={
                "finding": "Motherboard dañada",
                "new_scope": "PSU + MB",
                "revised_amount": Decimal("2000.00"),
                "evidence_notes": "",
            },
        )
        decide_scope_change(change=change, actor=self.client_user, approve=False)
        quote.refresh_from_db()
        self.assertEqual(quote.amount, Decimal("100.00"))
        self.assertEqual(change.status, ScopeChange.Status.REJECTED)


class PermissionViewTests(BaseFlowTestCase):
    def test_client_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/entrar/", response.url)

    def test_client_sees_own_requests_only(self):
        other_org = Organization.objects.create(
            name="Externo",
            org_type=Organization.OrgType.CLIENT,
            contact_email="e@example.com",
            zone="Sur",
        )
        other_user = User.objects.create_user(
            username="ext",
            password="pass12345",
            role=User.Role.CLIENT,
            organization=other_org,
        )
        ServiceRequest.objects.create(
            client=other_org,
            created_by=other_user,
            category=self.category,
            title="Ajena",
            description="No debe verse",
            location="Sur",
        )
        self.client.login(username="cliente1", password="pass12345")
        response = self.client.get(reverse("dashboard"))
        self.assertContains(response, "PC no enciende")
        self.assertNotContains(response, "Ajena")

    def test_register_creates_provider_profile(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "nuevoprov",
                "email": "np@example.com",
                "first_name": "Ana",
                "password1": "Segura123!",
                "password2": "Segura123!",
                "organization_name": "Ana Soporte",
                "phone": "555",
                "zone": "Centro",
                "role": "proveedor",
            },
        )
        self.assertEqual(response.status_code, 302)
        org = Organization.objects.get(name="Ana Soporte")
        self.assertEqual(org.org_type, Organization.OrgType.PROVIDER)
        self.assertTrue(hasattr(org, "provider_profile"))

    def test_quote_and_accept_via_http(self):
        self.client.login(username="prov1", password="pass12345")
        response = self.client.post(
            reverse("quote_create", args=[self.service_request.pk]),
            {
                "scope": "Cambio de PSU",
                "amount": "100.00",
                "estimated_time": "mismo día",
            },
        )
        self.assertEqual(response.status_code, 302)
        quote = Quote.objects.get(service_request=self.service_request)
        self.client.logout()
        self.client.login(username="cliente1", password="pass12345")
        response = self.client.post(
            reverse("quote_accept", args=[self.service_request.pk, quote.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.service_request.refresh_from_db()
        self.assertEqual(self.service_request.status, ServiceRequest.Status.ACCEPTED)
