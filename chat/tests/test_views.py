from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

from chat.models import Member, Session
from chat.usecases import SessionUseCase, CommonUseCase
from chat.views import SessionViewSet


class SessionViewTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="alpha",
            password="12345678!",
            email="alpha@site.com"
        )

        self.second_user = User.objects.create_user(
            username="beta",
            password="12345678!",
            email="beta@site.com"
        )

        self.user.save()

        self.factory = APIRequestFactory()
        self.view = SessionViewSet.as_view({
            'post': 'create',
            'patch': 'join',
        })

        self.session = Session.objects.create(user=self.user)

    def test_create(self):
        request = self.factory.post('/session/')
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.assertEqual(201, response.status_code)
        self.assertEqual(self.session.user.username, self.user.username)

    def test_failed_join_user_is_session_creator(self):
        request = self.factory.patch('/session/')
        force_authenticate(request, user=self.user)
        response = self.view(request, self.session.code)
        print(response)

        with self.assertRaises(Member.DoesNotExist):
            Member.objects.get(session__code=self.session.code)

    def test_pass_join(self):
        request = self.factory.patch('/session/')
        force_authenticate(request, user=self.second_user)
        response = self.view(request, self.session.code)
        print(response)

        member = Member.objects.get(session__code=self.session.code)

        self.assertEqual(200, response.status_code)
        self.assertEqual(member.user.username, self.second_user.username)




