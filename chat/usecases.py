from django.contrib.auth.models import User

from .models import Session, Message, Member
from .serializers import SessionSerializer, MessageSerializer, MemberSerializer


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

    def can_join_session(self, session_code):
        result = False

        try:
            Session.objects.get(user__username=self.user, code=session_code)
        except Session.DoesNotExist:
            result = True

        return result

    def join(self, session_code):
        if self.can_join_session(session_code):
            user = User.objects.get(username=self.user)
            session = Session.objects.get(code=session_code)
            serializer = MemberSerializer(data={"user": user.id, "session": session.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return session_code

        return session_code



