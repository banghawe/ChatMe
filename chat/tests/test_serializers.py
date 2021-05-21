from django.test import TestCase
from rest_framework.exceptions import ValidationError

from chat.serializers import RegisterSerializer


class RegisterSerializerTest(TestCase):
    def setUp(self) -> None:
        self.valid_data = {
            "username": "charlie12",
            "password": "12345678w!",
            "password2": "12345678w!",
            "email": "charlie12@site.com",
            "first_name": "new",
            "last_name": "user"
        }

        self.not_valid_data = {
            "username": "charlie12",
            "password": "12345678w!",
            "password2": "12345678w!!",
            "email": "charlie12@site.com",
            "first_name": "new",
            "last_name": "user"
        }

    def test_valid_retype_email(self):
        serializer = RegisterSerializer(data=self.valid_data)
        self.assertEqual(True, serializer.is_valid())

    def test_not_valid_retype_email(self):
        serializer = RegisterSerializer(data=self.not_valid_data)
        self.assertEqual(False, serializer.is_valid())

    def test_raise_error_not_valid_retype_email(self):
        serializer = RegisterSerializer(data=self.not_valid_data)

        self.assertRaisesRegex(ValidationError, "password didn't match!", serializer.is_valid, True)
