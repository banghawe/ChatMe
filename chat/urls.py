from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import RegisterView, SessionViewSet


urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('register', RegisterView.as_view(), name='auth_register'),
    path('session', SessionViewSet.as_view({
        'post': 'create',
        'patch': 'join',
    })),
]
