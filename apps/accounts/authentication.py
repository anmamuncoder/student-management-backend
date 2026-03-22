import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

# IAT = Issued At Time

class PasswordAwareJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication.

    Invalidates all existing tokens when:
    - User changes their password
    - User changes their email
    - Admin forces logout from all devices
    """

    def get_user(self, validated_token):
        # Step 1: get user normally
        user = super().get_user(validated_token)

        # Step 2: check if any security event occurred
        if user.token_invalidated_at:

            # Step 3: get token issued-at time
            token_iat = validated_token.get('iat')

            if token_iat:
                # Step 4: convert Unix timestamp to datetime
                token_issued_at = datetime.datetime.fromtimestamp(
                    token_iat,
                    tz=datetime.timezone.utc
                )

                # Step 5: was token issued before security event?
                if token_issued_at < user.token_invalidated_at:
                    raise InvalidToken(
                        "Token is invalid due to recent security change. "
                        "Please login again."
                    )

        return user
 