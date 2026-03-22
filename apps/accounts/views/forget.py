from .imports import *
from django.core.mail import send_mail


class ForgotPasswordAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        user = User.objects.filter(email=email).first()

        if user:
            otp = str(random.randint(100000, 999999))

            user.reset_password_otp = otp
            user.reset_password_otp_created_at = timezone.now()
            user.is_email_verified = False

            user.save(update_fields=[
                "reset_password_otp",
                "reset_password_otp_created_at",
                "is_email_verified"
            ])

            send_mail(
                "Password Reset OTP",
                f"Your OTP is {otp}",
                "noreply@example.com",
                [user.email],
            )
        return BaseResponse(success=True,message="If the email exists, a reset OTP has been sent",status=status.HTTP_202_ACCEPTED)
 

class VerifyResetOTPAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = VerifyResetOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        user = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError("Invalid request")

        if user.reset_password_otp != otp:
            raise ValidationError("Invalid OTP")

        expiry = user.reset_password_otp_created_at + timedelta(
            seconds=settings.RESET_OTP_EXPIRY
        )

        if timezone.now() > expiry:
            raise ValidationError("OTP expired")

        # ----------------------------
        # Generate reset token
        # ----------------------------
        token = secrets.token_urlsafe(32)

        user.reset_password_token = token
        user.reset_password_token_created_at = timezone.now()

        user.reset_password_otp = None

        user.is_email_verified = True
        user.email_verified_at = timezone.now()

        user.save(update_fields=[
            "reset_password_token",
            "reset_password_token_created_at",
            "reset_password_otp",

            "is_email_verified",
            "email_verified_at"
        ])

        return BaseResponse(
            data={"reset_token": token},
            message="OTP verified"
        )
            
class ResetPasswordAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["reset_token"]
        new_password = serializer.validated_data["new_password"]

        user = User.objects.filter(reset_password_token=token).first()

        if not user:
            raise ValidationError("Invalid reset token")

        expiry = user.reset_password_token_created_at + timedelta(seconds=settings.RESET_TOKEN_EXPIRY)

        if timezone.now() > expiry:
            raise ValidationError("Reset token expired")

        user.set_password(new_password)

        user.reset_password_token = None
        user.reset_password_token_created_at = None
        user.last_password_change = timezone.now()

        user.save(update_fields=[
            "password",
            "reset_password_token",
            "reset_password_token_created_at",
            "last_password_change"
        ])

        return BaseResponse(
            message="Password reset successful"
        )


# forgot-password
#     ↓
# send OTP
#     ↓
# verify-reset-otp
#     ↓
# generate reset_token  ← এখানে
#     ↓
# reset-password
