from django.test import TestCase
from accounts.models import User

class CustomUserTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(None, "test@test.com",
                                         "password")
        self.assertIsNotNone(user)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            user = User.objects.create_user(None, None, "password")