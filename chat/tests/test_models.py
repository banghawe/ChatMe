from django.test import TestCase
from chat.models import Session, Member
from django.contrib.auth.models import User


class SessionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username="alpha",
            password="12345678!",
            email="alpha@site.com"
        )

        Session.objects.create(user=user)

    def test_object_name_is_code(self):
        session = Session.objects.get(user__username="alpha")
        expected_name = str(session.code)

        self.assertEqual(str(session), expected_name)


class MemberModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username="alpha",
            password="12345678!",
            email="alpha@site.com"
        )

        session = Session.objects.create(user=user)
        Member.objects.create(
            session=session,
            user=user
        )

    def test_object_name_is_username_hyphen_code(self):
        member = Member.objects.get(id=1)
        expected_name = f"{member.user.username} - {str(member.session.code)}"

        self.assertEqual(str(member), expected_name)
