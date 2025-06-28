from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class TestUserRegistration(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.register_url = reverse("user-register")
        self.valid_payload = {
            "first_name": "Test",
            "last_name": "Tester",
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "password2": "testpass123",
        }

    def test_valid_registration(self) -> None:
        response = self.client.post(self.register_url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_email(self) -> None:
        payload = self.valid_payload.copy()
        payload["email"] = "invalid-email"
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_fields(self) -> None:
        response = self.client.post(self.register_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
