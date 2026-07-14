from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .services.google_auth_service import GoogleAuthService
from .services.oauth_credential_service import OAuthCredentialService


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        sociallogin.user = GoogleAuthService.get_or_create_user(sociallogin)
        OAuthCredentialService.create_or_update(sociallogin.user, sociallogin)
        sociallogin.save(request)
        return sociallogin.user
