from .imports import *


def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))


class EmailChangeRequestView(APIView):
    """
    POST /api/v1/accounts/email/change/
    Send OTP to new email address.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EmailChangeRequestSerializer(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)

        user      = request.user
        new_email = serializer.validated_data['new_email']
        otp       = generate_otp()

        user.pending_email              = new_email
        user.email_change_otp           = otp
        user.email_change_otp_created_at = timezone.now()

        user.save(update_fields=[
            'pending_email',
            'email_change_otp',
            'email_change_otp_created_at',
        ])

        send_mail(
            subject='Email Change OTP - AuthVault',
            message=f'Your email change OTP: {otp}\n',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[new_email],
            fail_silently=False,
        )

        return BaseResponse(
            success=True,
            message=f"OTP sent to {new_email}.",
            status=status.HTTP_200_OK
        )
 

class EmailChangeVerifyView(APIView):
    """
    POST /api/v1/accounts/email/verify/
    Verify OTP and update email.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EmailChangeVerifySerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user       = request.user
        user.email = user.pending_email

        user.pending_email               = None
        user.email_change_otp            = None
        user.email_change_otp_created_at = None
        user.email_changed_at            = timezone.now()
        user.token_invalidated_at = timezone.now()

        user.save(update_fields=[
            'email',
            'pending_email',
            'email_change_otp',
            'email_change_otp_created_at',
            'email_changed_at',
            'token_invalidated_at'
        ])

        return BaseResponse(
            success=True,
            message="Email updated successfully." ,
            status=status.HTTP_200_OK,
        )
 