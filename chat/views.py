from django.contrib.auth.models import User
from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import RegisterSerializer
from .usecases import SessionUseCase


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class SessionViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def create(request: Request):
        session = SessionUseCase(request.user)
        data = session.create()

        return Response(data, status=status.HTTP_201_CREATED)

    @staticmethod
    def join(request: Request, session_code: str):
        session = SessionUseCase(request.user)
        data = session.join(session_code)

        return Response({"message": data})

