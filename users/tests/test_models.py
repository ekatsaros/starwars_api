from django.test import TestCase

from users.models import ApiUser


class ApiUserTests(TestCase):
    def setUp(self) -> None:
        self.user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "testpass123",
            "username": "testuser",
        }
        self.user = ApiUser.objects.create_user(**self.user_data)

    def test_create_user(self) -> None:
        """Test creating a new user"""
        self.assertEqual(self.user.email, self.user_data["email"])
        self.assertEqual(self.user.username, self.user_data["username"])
        self.assertTrue(self.user.check_password(self.user_data["password"]))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)

    def test_create_superuser(self) -> None:
        """Test creating a new superuser"""
        admin_user = ApiUser.objects.create_superuser(
            first_name="User", last_name="User", email="admin@example.com", password="admin123", username="admin"
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)

    def test_user_str(self) -> None:
        """Test string representation of user"""
        self.assertEqual(str(self.user), self.user.email)
