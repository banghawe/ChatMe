import copy

from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound

from .models import Session, Message, Member
from .serializers import SessionSerializer, SessionMessageSerializer, MemberSerializer, MessageSerializer

from notifications.utils import notify
from notifications import default_settings as notifs_settings


class CommonUseCase:
    @staticmethod
    def is_user_exists(username):
        result = True
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            result = False

        return result


class SessionUseCase(CommonUseCase):
    def __init__(self, username):
        self.user = username

    def create(self):
        user = User.objects.get(username=self.user)
        serializer = SessionSerializer(data={"user": user.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return serializer.data

    @staticmethod
    def is_session_exists(session_code):
        try:
            return Session.objects.get(code=session_code) is not None
        except Session.DoesNotExist:
            raise NotFound("Session has not found", 404)

    def can_join_session(self, session_code):
        result = False

        try:
            Session.objects.get(user__username=self.user, code=session_code)
        except Session.DoesNotExist:
            result = True

        return result

    def join(self, session_code):
        if self.is_session_exists(session_code) and self.can_join_session(session_code):
            user = User.objects.get(username=self.user)
            session = Session.objects.get(code=session_code)
            serializer = MemberSerializer(data={"user": user.id, "session": session.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return session_code

        return session_code

    def retrieve(self, session_code):
        if self.is_user_exists(self.user) and self.is_session_exists(session_code):
            session = Session.objects.get(code=session_code)
            serializer = SessionMessageSerializer(session)

            return serializer.data

    def create_message(self, session_code, data: MessageSerializer.data):
        if self.is_user_exists(self.user) and self.is_session_exists(session_code):
            session = Session.objects.get(code=session_code)
            user = User.objects.get(username=self.user)

            new_data = copy.deepcopy(data)
            new_data["session"] = session.id
            new_data["user"] = user.id

            serializer = MessageSerializer(data=new_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            notif_args = {
                'source': user,
                'source_display_name': user.get_full_name(),
                'category': 'chat', 'action': 'Sent',
                'obj': session.id,
                'short_description': 'You have a new message', 'silent': True,
                'extra_data': {
                    notifs_settings.NOTIFICATIONS_WEBSOCKET_URL_PARAM: str(session.code),
                    'message': serializer.data
                }
            }

            notify(**notif_args, channels=['websocket'])

            return serializer.data



