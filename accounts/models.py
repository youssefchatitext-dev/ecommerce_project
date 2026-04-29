from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid


def pending_signup_expiry():
    return timezone.now() + timezone.timedelta(hours=24)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    email_verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile<{self.user.username}>"


class PendingSignup(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=pending_signup_expiry)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"PendingSignup<{self.username}>"
