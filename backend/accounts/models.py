from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    email = models.EmailField(unique=True)
    intro = models.TextField(null=True, blank=True)
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]