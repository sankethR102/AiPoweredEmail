from django.contrib.auth import get_user_model


User = get_user_model()


class GoogleAuthService:
    @staticmethod
    def get_or_create_user(sociallogin):
        extra_data = sociallogin.account.extra_data

        email = extra_data.get("email")
        given_name = extra_data.get("given_name", "")
        family_name = extra_data.get("family_name", "")

        if not email:
            raise ValueError("Google account email is required.")

        user = User.objects.filter(email=email).first()
        if user:
            return user
        

        return User.objects.create_user(
            email=email,
            first_name=given_name,
            last_name=family_name,
            auth_provider=User.AuthProvider.GOOGLE,
        )
