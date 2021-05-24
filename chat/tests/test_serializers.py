from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from chat.models import Session, Member, Message
from chat.serializers import RegisterSerializer, SessionMessageSerializer


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


class SessionMessageSerializerTest(TestCase):
    def setUp(self) -> None:
        self.first_user = User.objects.create_user(
            username="alpha",
            password="12345678!",
            email="alpha@site.com"
        )

        self.second_user = User.objects.create_user(
            username="beta",
            password="12345678!",
            email="beta@site.com"
        )

        self.session = Session.objects.create(user=self.first_user)
        Member.objects.create(user=self.second_user, session=self.session)

    def test_nested_session_message_serializer(self):
        Message.objects.create(user=self.first_user, session=self.session, message="hallo beta")
        Message.objects.create(user=self.second_user, session=self.session, message="hallo alpha")
        Message.objects.create(user=self.first_user, session=self.session, message="ada")

        serializer = SessionMessageSerializer(self.session)

        self.assertTrue(len(serializer.data["messages"]) == 3)
