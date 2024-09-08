from django.contrib import admin
from .models import User

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

admin.site.unregister(OutstandingToken)
admin.site.register(User)