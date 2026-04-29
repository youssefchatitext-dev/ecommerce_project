from django.contrib import admin

from .models import PendingSignup, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_verified', 'updated_at')
    list_filter = ('email_verified',)
    search_fields = ('user__username', 'user__email')


@admin.register(PendingSignup)
class PendingSignupAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'created_at', 'expires_at')
    search_fields = ('username', 'email')
