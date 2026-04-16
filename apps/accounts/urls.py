import django 
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterAPIView,
    LoginAPIView,
    VerifyOTPAPIView,
    ResendOTPAPIView,
    TokenRefreshAPIView,

    ForgotPasswordAPIView,
    VerifyResetOTPAPIView,
    ResetPasswordAPIView,

    EmailChangeRequestView, 
    EmailChangeVerifyView,
    PasswordChangeView,

    RankViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register(r'ranks', RankViewSet, basename='ranks')
router.register(r'users', UserViewSet, basename='users')
 

app_name = 'accounts'
urlpatterns = [ 

    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('refresh/', TokenRefreshAPIView.as_view(), name='token_refresh'),

    # email verification system
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='verify_otp'),
    path("resend-otp/", ResendOTPAPIView.as_view(), name="resend_otp"),

    path("forgot-password/", ForgotPasswordAPIView.as_view()),
    path("verify-reset-otp/", VerifyResetOTPAPIView.as_view()),
    path("reset-password/", ResetPasswordAPIView.as_view()),

    # authenticated apis
    path('password/change/', PasswordChangeView.as_view(), name='password-change'),
    path('email/change/', EmailChangeRequestView.as_view(), name='email-change-request'),
    path('email/change/verify/', EmailChangeVerifyView.as_view(), name='email-change-verify'),

] + router.urls

# /api/v1/accounts/password/change/
# /api/v1/accounts/email/change/
# /api/v1/accounts/email/change/verify/

# /api/v1/accounts/profile/update/​
# /api/v1/accounts/profile/

# /api/v1/accounts/phone/change/​
# /api/v1/accounts/delete/​
# /api/v1/accounts/deactivate/