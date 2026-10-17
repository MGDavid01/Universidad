from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from api.models import Account, Bank, Payment, Provider


class AccountDetailAPIViewTests(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.url = reverse("api:account-detail", kwargs={"pk": 3})

	def test_missing_account_returns_404(self):
		response = self.client.get(self.url)

		self.assertEqual(response.status_code, 404)

	def test_existing_account_returns_detail(self):
		user = User.objects.create_user(
			username="account-owner",
			first_name="Test",
			last_name="Owner",
		)
		bank = Bank.objects.create(name="Test bank", address="Test address")
		account = Account.objects.create(
			pk=3,
			name="Test account",
			bank=bank,
			user=user,
			currency="MXN",
		)

		response = self.client.get(self.url)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data["id"], account.pk)
		self.assertEqual(response.data["name"], account.name)
		self.assertEqual(response.data["bank_name"], bank.name)
		self.assertEqual(response.data["username"], user.username)


class UpdateAPIViewTests(TestCase):
	def setUp(self):
		self.client = APIClient()
		user = User.objects.create_user(username="update-owner")
		bank = Bank.objects.create(name="Test bank", address="Test address")
		account = Account.objects.create(
			name="Test account",
			bank=bank,
			user=user,
			currency="MXN",
		)
		provider = Provider.objects.create(name="Test provider", address="Test address")
		payment = Payment.objects.create(
			name="Test payment",
			account=account,
			user=user,
			provider=provider,
		)
		self.update_cases = [
			(f"/v1/bank/update/{bank.pk}/", {"name": "Updated bank"}),
			(f"/v1/account/update/{account.pk}/", {"name": "Updated account"}),
			(f"/v1/provider/update/{provider.pk}/", {"name": "Updated provider"}),
			(f"/v1/payment/update/{payment.pk}/", {"name": "Updated payment"}),
		]

	def test_all_update_endpoints_accept_patch(self):
		for url, data in self.update_cases:
			with self.subTest(url=url):
				response = self.client.patch(url, data, format="json")

				self.assertEqual(response.status_code, 200)
				self.assertEqual(response.data["name"], data["name"])

	def test_get_on_all_update_endpoints_returns_the_requested_object(self):
		for url, _ in self.update_cases:
			with self.subTest(url=url):
				response = self.client.get(url)

				self.assertEqual(response.status_code, 200)
				self.assertIn("id", response.data)

	def test_account_get_returns_its_related_bank_and_user(self):
		url, _ = self.update_cases[1]

		response = self.client.get(url)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data["bank_name"], "Test bank")
		self.assertEqual(response.data["username"], "update-owner")

	def test_get_for_missing_object_returns_404(self):
		response = self.client.get("/v1/bank/update/999999/")

		self.assertEqual(response.status_code, 404)

	def test_bank_update_uses_update_serializer(self):
		url, _ = self.update_cases[0]

		response = self.client.patch(url, {"name": "Updated bank"}, format="json")

		self.assertEqual(response.status_code, 200)
		self.assertNotIn("id", response.data)
		self.assertNotIn("timestamp", response.data)
		self.assertNotIn("update", response.data)

	def test_bank_update_accepts_put(self):
		url, _ = self.update_cases[0]

		response = self.client.put(
			url,
			{"name": "Replaced bank", "address": "New address", "status": False},
			format="json",
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data["name"], "Replaced bank")
