from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from .views import *

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path('signin/', TokenObtainPairView.as_view(), name="signin"),
    path("signout/", TokenBlacklistView.as_view(), name="signout"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("<str:username>/", UserDetailAPIView.as_view(), name="user-detail"),
]