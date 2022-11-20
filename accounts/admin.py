from django.contrib import admin
from .models import CustomUser, Notice

admin.site.register(CustomUser)
admin.site.register(Notice)