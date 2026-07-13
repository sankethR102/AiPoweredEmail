from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver

@receiver(pre_social_login)
def handle_google_login(request, sociallogin, **kwargs):
    print("=" * 50)
    print("EMAIL:", sociallogin.user.email)
    print("EXTRA DATA:", sociallogin.account.extra_data)
    print(sociallogin.token.__dict__)
    print("=" * 50)