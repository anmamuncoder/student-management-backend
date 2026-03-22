from .imports import *

 
# --------------------------
# Token Refresh View
# --------------------------
class TokenRefreshAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        refresh_token = request.data.get("refresh")

        if not refresh_token:
            raise ValidationError("Refresh token required")

        try:
            refresh = RefreshToken(refresh_token)

            data = {
                "access": str(refresh.access_token)
            }

            return BaseResponse(
                data=data,
                message="Access token generated",
                success=True,
                status=status.HTTP_200_OK
            )

        except Exception:
            raise ValidationError("Invalid refresh token")


# --------------------------
# Login View 
# --------------------------
class LoginAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # --------------------------
        # If OTP login enabled
        # --------------------------
        if not user.is_email_verified or settings.AUTH_OTP_ENABLED: 
            try: 
                otp = user.generate_otp()
                send_mail(
                    "Your OTP Code",
                    f"Your OTP is {otp}",
                    "noreply@example.com",
                    [user.email],
                )
            except Exception as e:
                raise ValidationError("Email send failed")

            return BaseResponse(
                message="OTP sent to your email",
                success=True,
                status=status.HTTP_200_OK
            )
        
        # --------------------------
        # Direct login
        # --------------------------
        refresh = RefreshToken.for_user(user)
        
        user.last_login = timezone.now()
        user.failed_login_attempts = 0
        user.save(update_fields=["last_login",'failed_login_attempts'])

        data = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

        return BaseResponse(
            data=data,
            message="Login successful",
            success=True,
            status=status.HTTP_200_OK
        )

