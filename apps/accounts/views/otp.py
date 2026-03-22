from .imports import *
from apps.accounts.throttles import ForgotPasswordThrottle

# ----------------------------------------
# OTP Verification View
# ----------------------------------------

class VerifyOTPAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        user = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError("User not found")
        
        # OTP match
        if user.otp != otp:
            raise ValidationError("Invalid OTP")

        # OTP expiry check
        expiry_time = user.otp_created_at + timedelta(seconds=settings.OTP_EXPIRY_TIME)

        if timezone.now() > expiry_time:
            raise ValidationError("OTP expired")

        # clear otp
        user.otp = None
        user.is_email_verified = True
        user.email_verified_at = timezone.now()
        user.save(update_fields=["otp",'is_email_verified','email_verified_at'])

        refresh = RefreshToken.for_user(user)

        data = {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }

        return BaseResponse(
            data=data,
            message="OTP verified successfully",
            success=True,
            status=status.HTTP_200_OK
        )

# ----------------------------------------
# Resend OTP View
# ----------------------------------------

class ResendOTPAPIView(APIView):
    throttle_classes = [ForgotPasswordThrottle]
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ResendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        user = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError("User not found")

        # resend cooldown check
        if user.otp_created_at:

            cooldown = user.otp_created_at + timedelta(seconds=settings.OTP_RESEND_COOLDOWN)

            if timezone.now() < cooldown:
                # remaining = cooldown - timezone.now()
                # seconds = int(remaining.total_seconds())
                raise ValidationError({"message": "Please wait before requesting another OTP", })
            
        otp = user.generate_otp()

        try:
            send_mail("Your OTP Code",f"Your OTP is {otp}","noreply@example.com",[user.email],)

        except Exception:
            raise ValidationError("OTP sending failed")

        return BaseResponse(
            message="OTP resent successfully",
            success=True,
            status=status.HTTP_200_OK
        )


    