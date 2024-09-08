from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse
import requests

from .serializers import UserSerializer, ChangePasswordSerializer

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        self.permission_classes = [IsAuthenticated]
        
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
        serializer = UserSerializer(user, context={'request': request})
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
    
    
class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password has been changed successfully."}, status=200)
        
        return Response(serializer.errors, status=400)