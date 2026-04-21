import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random
from django.utils import timezone

from kernel.models import BaseModel

from .constants import Gender, BloodGroup, MaritalStatus, Wing, CurrentStatus

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
 
        extra_fields.setdefault("is_email_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        user = self.create_user(email, password, **extra_fields)
 
        user.is_email_verified = True
        user.email_verified_at = timezone.now()
        user.save(update_fields=["is_email_verified", "email_verified_at"])

        return user

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
    # -------------------------
    # Identity
    # -------------------------
    personal_number = models.CharField(max_length=50, unique=True,null=True, blank=True)

    full_name = models.CharField(max_length=150, blank=True, null=True)
    short_name = models.CharField(max_length=100, blank=True, null=True)

    # -------------------------
    # Rank / Role
    # -------------------------
    rank = models.ForeignKey("accounts.Rank", on_delete=models.SET_NULL, null=True, blank=True)
  
    # -------------------------
    # Contact
    # -------------------------
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    national_id = models.CharField(max_length=50, blank=True, null=True)

    # -------------------------
    # Personal Info
    # -------------------------
    gender = models.CharField(max_length=10,choices=Gender.choices,blank=True,null=True,)
    blood_group = models.CharField(max_length=5, choices=BloodGroup.choices, blank=True, null=True,)
    marital_status = models.CharField(max_length=20, choices=MaritalStatus.choices, null=True,)

    date_of_marriage = models.DateField(blank=True, null=True)

    # -------------------------
    # Birth Info
    # -------------------------
    birth_date = models.DateField(blank=True, null=True)
    place_of_birth = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    religion = models.CharField(max_length=50, blank=True, null=True)

    # -------------------------
    # Address
    # -------------------------
    present_address = models.TextField(blank=True, null=True)
    permanent_address = models.TextField(blank=True, null=True)

    # -------------------------
    # Organization Info
    # -------------------------
    current_unit = models.CharField(max_length=100, blank=True, null=True)
    parent_unit_auth = models.CharField(max_length=100, blank=True, null=True)

    wing = models.CharField(max_length=20, choices=Wing.choices, blank=True, null=True,)

    appointment = models.CharField(max_length=100, blank=True, null=True)

    joining_date = models.DateField(blank=True, null=True)
    date_of_enrolment = models.DateField(blank=True, null=True)

    current_status = models.CharField(max_length=20, choices=CurrentStatus.choices, default=CurrentStatus.ACTIVE, blank=True, null=True,)

    # -------------------------
    # Files
    # -------------------------
    photo = models.ImageField(upload_to="users/photos/", blank=True, null=True)
    resume = models.FileField(upload_to="users/resume/", blank=True, null=True)

    def __str__(self):
        return f"{self.email} "

    class Meta:
        db_table = "users"

class Rank(BaseModel):
    code = models.CharField(max_length=20, unique=True)  
    name = models.CharField(max_length=100)              
    order = models.PositiveIntegerField(default=0)     
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name




