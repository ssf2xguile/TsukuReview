from django.contrib import admin
from .models import CustomUser, Notice

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'college', 'is_active', 'is_staff', 'is_superuser', 'last_login')
    list_display_links = ('username', 'email')
    list_filter = ('college', 'is_staff', 'is_superuser', 'is_active')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Notice)