
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from django.urls import reverse
import requests

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
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