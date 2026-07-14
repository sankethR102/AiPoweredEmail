from django.db import transaction

from accounts.models import OAuthCredential


class OAuthCredentialService:
    
    @staticmethod
    @transaction.atomic
    def create_or_update(user, sociallogin):
        provider = sociallogin.account.provider
        provider_user_id = sociallogin.account.uid
        refresh_token = getattr(sociallogin.token, "token_secret", None)

        credential = (
            OAuthCredential.objects.select_for_update()
            .filter(
                provider=provider,
                provider_user_id=provider_user_id,
            )
            .first()
        )

        if credential:
            if refresh_token:
                credential.refresh_token = refresh_token
                credential.save(update_fields=["refresh_token", "updated_at"])
            return credential

        return OAuthCredential.objects.create(
            user=user,
            provider=provider,
            provider_user_id=provider_user_id,
            refresh_token=refresh_token,
        )
