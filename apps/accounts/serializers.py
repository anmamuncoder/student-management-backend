from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Rank, User
from django.conf import settings

# ----------------------------------------
# Registration Serializer
# ----------------------------------------

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user

# ----------------------------------------
# Login Serializer
# ----------------------------------------

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            try:
                user_obj = User.objects.get(email=email)
                user_obj.failed_login_attempts += 1
                user_obj.save(update_fields=['failed_login_attempts'])
            except User.DoesNotExist:
                pass
            
            raise serializers.ValidationError("Invalid credentials")

        attrs["user"] = user
        return attrs
# ----------------------------------------
# OTP Verification Serializer
# ----------------------------------------

class VerifyOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


# ----------------------------------------
# Resend OTP Serializer
# ----------------------------------------

class ResendOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()




# ----------------------------------------
# Forget Passwrod
# ----------------------------------------
class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()


class VerifyResetOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()
    otp = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):

    reset_token = serializers.CharField()
    new_password = serializers.CharField(min_length=6)


# ----------------------------------------
# Passsword change
# ----------------------------------------
class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password     = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "New passwords do not match."})
        if attrs['current_password'] == attrs['new_password']:
            raise serializers.ValidationError({"new_password": "New password must be different from current password."})
        return attrs
    

# ----------------------------------------
# Email change
# ----------------------------------------
from django.utils import timezone
from datetime import timedelta

class EmailChangeRequestSerializer(serializers.Serializer):
    new_email = serializers.EmailField()
    password  = serializers.CharField(write_only=True)

    def validate_new_email(self, value):
        user = self.context['request'].user
        if value == user.email:
            raise serializers.ValidationError("New email must be different from current email.")
        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['password']):
            raise serializers.ValidationError({"password": "Incorrect password."})
        return attrs


class EmailChangeVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=64)

    def validate_otp(self, value):
        user = self.context['request'].user

        if not user.pending_email:
            raise serializers.ValidationError("No pending email change request found.")
        if not user.email_change_otp:
            raise serializers.ValidationError("OTP not found. Please request again.")

        otp_expiry = user.email_change_otp_created_at + timedelta(seconds=settings.OTP_EXPIRY_TIME)

        if timezone.now() > otp_expiry:
            raise serializers.ValidationError("OTP has expired. Please request again.")
        if user.email_change_otp != value:
            raise serializers.ValidationError("Invalid OTP.")
        return value


# ----------------------------------------
# Rank Serializer
# ----------------------------------------
class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)
    role_slug = serializers.CharField(write_only=True, required=False)

    user_role = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = [
            # -------------------------
            # Identity
            # -------------------------
            "id",
            "personal_number",
            "full_name",
            "short_name",

            # -------------------------
            # Contact
            # -------------------------
            "email",
            "phone",
            "national_id",

            # -------------------------
            # Rank / Role
            # -------------------------
            "rank",

            # -------------------------
            # Personal Info
            # -------------------------
            "age",
            "gender",
            "blood_group",
            "marital_status",
            "date_of_marriage",

            # -------------------------
            # Birth Info
            # -------------------------
            "birth_date",
            "place_of_birth",
            "country",
            "religion",

            # -------------------------
            # Address
            # -------------------------
            "present_address",
            "permanent_address",

            # -------------------------
            # Organization Info
            # -------------------------
            "current_unit",
            "parent_unit_auth",
            "wing",
            "appointment",
            "joining_date",
            "date_of_enrolment",
            "current_status",

            # -------------------------
            # Files
            # -------------------------
            "photo",
            "resume",
            # -------------------------
            # Auth / Extra
            # -------------------------
            "password",
            "role_slug",
            "user_role",
        ]

    def get_user_role(self, obj):
        roles = [ur.role.slug for ur in obj.user_roles.all()]

        if hasattr(obj, "student"):
            roles.append("student")

        return roles
    
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        role_slug = validated_data.pop("role_slug", None)

        user = User(**validated_data)

        if password:
            user.set_password(password)

        user.save()

        # assign role
        if role_slug:
            from apps.rbac.models import Role, UserRole
            role = Role.objects.get(slug=role_slug)
            UserRole.objects.create(user=user, role=role)

        return user

    def update(self, instance, validated_data):
        # BLOCK password update
        validated_data.pop("password", None)

        return super().update(instance, validated_data)