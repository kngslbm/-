from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse
import requests

from .serializers import UserSerializer

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data, context={'request': request})
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
        return Response(serializer.errors, status=400)

    def delete(self, request, username):
        password = request.data.get("password")
        if not password:
            return Response({"error": "password is required"}, status=400)
        if not request.user.check_password(password):
            return Response({"error": "password is incorrect"}, status=400)
        request.user.delete()
        return Response(status=204)
    
    
class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, username):
        user = get_object_or_404(get_user_model(), username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)
    
    def put(self, request, username):
        user = get_object_or_404(get_user_model(), username=username)
        if request.user != user:
            return Response({"error": "permission denied"}, status=403)
        serializer = UserSerializer(instance=user, data=request.data, context={'request': request}, partial=True)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)