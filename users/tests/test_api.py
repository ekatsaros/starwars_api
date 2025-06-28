from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

# import the ApiUser model from test models
from users.models import ApiUser


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
        }

    def test_valid_registration(self) -> None:
        response = self.client.post(self.register_url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_token_creation(self) -> None:
        """Test that token is created for user"""
        self.client.post(self.register_url, self.valid_payload, format="json")
        user = ApiUser.objects.get(email=self.valid_payload["email"])
        token = Token.objects.get(user=user)
        self.assertIsNotNone(token)

    def test_invalid_email(self) -> None:
        payload = self.valid_payload.copy()
        payload["email"] = "invalid-email"
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_fields(self) -> None:
        response = self.client.post(self.register_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUserLogin(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.login_url = reverse("user-login")
        self.user = ApiUser.objects.create_user(
            first_name="Test",
            last_name="Tester",
            username="testuser",
            email="test@email.com",
            password="testpass123",
        )
        self.valid_login_payload = {
            "email": self.user.email,
            "password": "testpass123",
        }

    def test_valid_login(self) -> None:
        response = self.client.post(self.login_url, self.valid_login_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn("Authorization", response.headers)
        token = response.headers["Authorization"].split(" ")[1]
        self.assertTrue(Token.objects.filter(key=token).exists())

    def test_invalid_login(self) -> None:
        invalid_payload = {
            "email": "invalid@email.com",
            "password": "wrongpassword",
        }
        response = self.client.post(self.login_url, invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("Authorization", response.headers)
        self.assertEqual(response.json(), {"detail": "Invalid credentials"})
