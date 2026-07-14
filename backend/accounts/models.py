from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class User(AbstractUser):

    class AuthProvider(models.TextChoices):
        MANUAL = "manual", "Manual"
        GOOGLE = "google", "Google"

    username = None

    email = models.EmailField(unique=True)

    auth_provider = models.CharField(
        max_length=20,
        choices=AuthProvider.choices,
        default=AuthProvider.MANUAL,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class OAuthCredential(models.Model):

    class Provider(models.TextChoices):
        GOOGLE = "google", "Google"

    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="oauth_credentials",
    )
    provider = models.CharField(
        max_length=20,
        choices=Provider.choices,
    )
    provider_user_id = models.CharField(max_length=255)
    refresh_token = models.TextField(
    blank=True,
    null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("provider", "provider_user_id"),
                name="unique_oauth_provider_user_id",
            )
        ]
        ordering = ["-created_at"]


    def __str__(self):
        return f"{self.provider}:{self.provider_user_id} ({self.user.email})"
