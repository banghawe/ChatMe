from django.contrib.auth.models import User
from django.test import TestCase

from chat.models import Member, Session
from chat.usecases import SessionUseCase, CommonUseCase
from rest_framework.exceptions import NotFound


class CommonUseCaseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username="alpha",
            password="12345678!",
            email="alpha@site.com"
        )

    def test_is_user_exist(self):
        self.assertEqual(True, CommonUseCase.is_user_exists("alpha"))

    def test_is_user_not_exists(self):
        self.assertEqual(False, CommonUseCase.is_user_exists("charlie"))


class SessionUseCaseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username="alpha",
            password="12345678!",
            email="alpha@site.com"
        )

        User.objects.create_user(
            username="beta",
            password="12345678!",
            email="beta@site.com"
        )

    def test_pass_is_session_exists(self):
        first_user = User.objects.get(username="alpha")
        session = Session.objects.create(user=first_user)

        self.assertEqual(True, SessionUseCase.is_session_exists(session.code))

    def test_failed_is_session_exists(self):
        session_code = "083bd39f-1ddc-4f94-b12f-ca9904e2985a"

        with self.assertRaises(NotFound):
            SessionUseCase.is_session_exists(session_code)

    def test_create(self):
        user = User.objects.get(username="alpha")
        session = SessionUseCase(user.username)
        data = session.create()
        print(data)

        self.assertTrue(data is not None)
        self.assertEqual(user.id, data["user"])

    def test_false_can_join(self):
        user = User.objects.get(username="alpha")
        session = SessionUseCase(user.username)
        data = session.create()

        same_session = SessionUseCase(user.username)
        result = same_session.can_join_session(data["code"])

        self.assertEqual(False, result)

    def test_true_can_join(self):
        first_user = User.objects.get(username="alpha")
        second_user = User.objects.get(username="beta")

        session = SessionUseCase(first_user.username)
        data = session.create()

        same_session = SessionUseCase(second_user.username)
        result = same_session.can_join_session(data["code"])

        self.assertEqual(True, result)

    def test_failed_join(self):
        user = User.objects.get(username="alpha")
        session = SessionUseCase(user.username)
        data = session.create()

        same_session = SessionUseCase(user.username)
        same_session.join(data["code"])

        with self.assertRaises(Member.DoesNotExist):
            Member.objects.get(user=user, session_id=data["id"])

    def test_failed_join_session_not_found(self):
        session_code = "083bd39f-1ddc-4f94-b12f-ca9904e2985a"
        second_user = User.objects.get(username="beta")
        same_session = SessionUseCase(second_user.username)

        with self.assertRaises(NotFound):
            same_session.join(session_code)

    def test_pass_join(self):
        first_user = User.objects.get(username="alpha")
        second_user = User.objects.get(username="beta")
        session = SessionUseCase(first_user.username)
        data = session.create()

        same_session = SessionUseCase(second_user.username)
        same_session.join(data["code"])

        member = Member.objects.get(user=second_user, session_id=data["id"])

        self.assertEqual(second_user.id, member.user.id)

    def test_retrieve(self):
        first_user = User.objects.get(username="alpha")
        session = SessionUseCase(first_user.username)
        data = session.create()

        result = session.retrieve(data["code"])

        self.assertIn("messages", result)

    def test_pass_create_message(self):
        message = "message"

        first_user = User.objects.get(username="alpha")
        session = SessionUseCase(first_user.username)
        data = session.create()

        result = session.create_message(data["code"], {"message": message})

        self.assertEqual(message, result["message"])





