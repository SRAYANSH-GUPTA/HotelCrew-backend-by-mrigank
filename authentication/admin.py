from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'user_name', 'is_staff', 'is_active', 'created_at')
    search_fields = ('email', 'user_name')
    ordering = ('email',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(EmailOTP)
class EmailOTPModelAdmin(admin.ModelAdmin):
    list_display = ('email', 'otp', 'otp_created_at', 'forgot')
    search_fields = ('email',)
    ordering = ('email',)
