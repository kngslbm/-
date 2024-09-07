from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from .views import *

urlpatterns = [
    path("register/", RegisterAPIView.as_view()),
    path('signin/', TokenObtainPairView.as_view(), name="signin"),
    path("signout/", TokenBlacklistView.as_view(), name="signout"),
    path('token/refresh/', TokenRefreshView.as_view()),
    path("change-password/", ChangePasswordAPIView.as_view()),
    path("<str:username>/", UserDetailAPIView.as_view()),
]