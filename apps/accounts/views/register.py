from .imports import *
from rest_framework_simplejwt.tokens import RefreshToken  

# Create your views here.
# --------------------------
# Registration View
# --------------------------
class RegisterAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer) # user save

        user = serializer.save()
        data = serializer.data

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        
        if settings.AUTO_LOGIN_AFTER_REGISTRATION:
            data = {
                "access": str(access_token)
            }

        return BaseResponse(
            data=data,
            message="User registered successfully",
            success=True,
            status=status.HTTP_201_CREATED
        ) 
