# Django Imports for use urls in views

from .register import RegisterAPIView
from .login import LoginAPIView, TokenRefreshAPIView
from .otp import VerifyOTPAPIView, ResendOTPAPIView

from .forget import ForgotPasswordAPIView, VerifyResetOTPAPIView, ResetPasswordAPIView

from .email import EmailChangeRequestView, EmailChangeVerifyView
from .password import PasswordChangeView
from .ranks import RankViewSet, UserViewSet