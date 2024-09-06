from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *

urlpatterns = [
    path("registration/", RegisterAPIView.as_view()),
    path('signin/', TokenObtainPairView.as_view(), name="signin"),
    path('token/refresh/', TokenRefreshView.as_view()),
]