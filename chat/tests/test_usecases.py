from django.contrib.auth.models import User
from django.test import TestCase

from chat.models import Member
from chat.usecases import SessionUseCase, CommonUseCase


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

    def test_pass_join(self):
        first_user = User.objects.get(username="alpha")
        second_user = User.objects.get(username="beta")
        session = SessionUseCase(first_user.username)
        data = session.create()

        same_session = SessionUseCase(second_user.username)
        same_session.join(data["code"])

        member = Member.objects.get(user=second_user, session_id=data["id"])

        self.assertEqual(second_user.id, member.user.id)


