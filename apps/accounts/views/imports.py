# Django Imports

from django.shortcuts import render
from django.conf import settings 
from django.core.mail import send_mail
from django.utils import timezone

from rest_framework import generics, status, status
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError   

from datetime import timedelta
import random
import secrets 
import string

# Internal Imports
from apps.accounts.models import User
from apps.accounts.serializers import (
    RegisterSerializer, 
    LoginSerializer, 
    VerifyOTPSerializer, 
    ResendOTPSerializer,

    ForgotPasswordSerializer,
    VerifyResetOTPSerializer,
    ResetPasswordSerializer,

    PasswordChangeSerializer,

    EmailChangeRequestSerializer,
    EmailChangeVerifySerializer,  
)

# Base Utility
from kernel.responses import BaseResponse

