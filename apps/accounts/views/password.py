from .imports import *

class PasswordChangeView(APIView):
    """
    PUT /api/v1/accounts/password/change/
    Verify current password and set new password.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = PasswordChangeSerializer(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.password_changed_at = timezone.now()
        user.token_invalidated_at = timezone.now()

        user.save(update_fields=['password', 'password_changed_at','token_invalidated_at'])

        return BaseResponse(
            success=True,
            message="Password updated successfully.",
            status=status.HTTP_200_OK
        )
 