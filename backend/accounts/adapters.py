from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .services.google_auth_service import GoogleAuthService


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        sociallogin.user = GoogleAuthService.get_or_create_user(sociallogin)
        sociallogin.save(request)
        return sociallogin.user
