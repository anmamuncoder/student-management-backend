import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random
from django.utils import timezone

from kernel.models import BaseModel

from .constants import Gender

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")

        email = self.normalize_email(email)

        extra_fields.setdefault("is_active", True)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class BaseUser(AbstractBaseUser, PermissionsMixin, BaseModel):

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
 
    phone = models.CharField(max_length=20, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)

    gender = models.CharField(choices=Gender.choices, max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    # email verification with OTP fields
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True, blank=True)

    # Rest Password Process
    reset_password_otp = models.CharField(max_length=6, null=True, blank=True)
    reset_password_otp_created_at = models.DateTimeField(null=True, blank=True)

    reset_password_token = models.CharField(max_length=255, null=True, blank=True)
    reset_password_token_created_at = models.DateTimeField(null=True, blank=True)
    
    # security
    failed_login_attempts = models.IntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    last_password_change = models.DateTimeField(null=True, blank=True)

    # Email Change
    pending_email = models.EmailField(null=True, blank=True)
    email_change_otp = models.CharField(max_length=64, null=True, blank=True) 
    email_change_otp_created_at = models.DateTimeField(null=True, blank=True) 
    email_changed_at = models.DateTimeField(null=True, blank=True) 
    
    # Password
    password_changed_at = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # record when login
    last_login = models.DateTimeField(null=True, blank=True)
    # last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    # JWT token validation
    token_invalidated_at = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def generate_otp(self):
        otp = str(random.randint(100000, 999999))
        self.otp = otp
        self.otp_created_at = timezone.now()
        self.save(update_fields=["otp", "otp_created_at"])
        return otp
    
    def __str__(self):
        return self.email

class User(BaseUser):

    photo = models.ImageField(upload_to="users/profile/", blank=True, null=True)

    class Meta:
        db_table = "users"

