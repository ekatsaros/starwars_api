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
        self.assertTrue(self.user.check_password(self.user_data["password"]))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self) -> None:
        """Test creating a new superuser"""
        superuser = ApiUser.objects.create_superuser("admin@example.com", "admin", "FirstName", "LastName", "admin123")
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
