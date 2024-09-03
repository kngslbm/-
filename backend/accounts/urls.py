from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('signin/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]