
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse
import requests

from .serializers import UserSerializer

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {
                "username": serializer.data["username"],
                "password": request.data["password1"]
            }
            signin_url = request.build_absolute_uri(reverse("signin"))
            response = requests.post(signin_url, data)
        
            if response.status_code == 200:
                return Response(response.json(), status=200)
            else:
                return Response(response.text, status=response.status_code)

class UserDetailAPIView(APIView):
    def get(self, request, username):
        user = get_object_or_404(get_user_model(), username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)
                