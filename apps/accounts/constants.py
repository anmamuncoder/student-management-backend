from django.db import models
 
# -------------------------------
# Gender
# -------------------------------
class Gender(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    OTHER = "other", "Other"


# -------------------------------
# Blood Group
# -------------------------------
class BloodGroup(models.TextChoices):
    A_POS = "A+", "A+"
    A_NEG = "A-", "A-"
    B_POS = "B+", "B+"
    B_NEG = "B-", "B-"
    AB_POS = "AB+", "AB+"
    AB_NEG = "AB-", "AB-"
    O_POS = "O+", "O+"
    O_NEG = "O-", "O-"


# -------------------------------
# Marital Status
# -------------------------------
class MaritalStatus(models.TextChoices):
    SINGLE = "single", "Single"
    MARRIED = "married", "Married"
    DIVORCED = "divorced", "Divorced"
    WIDOWED = "widowed", "Widowed"


# -------------------------------
# Wing
# -------------------------------
class Wing(models.TextChoices):
    ARMY = "army", "Army"
    NAVY = "navy", "Navy"
    AIR_FORCE = "air_force", "Air Force"
    CIVIL = "civil", "Civil"
    SCHOOL = "school", "School"


# -------------------------------
# Current Status
# -------------------------------
class CurrentStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    RETIRED = "retired", "Retired"
    SUSPENDED = "suspended", "Suspended"


# -------------------------------
# Qualification Type
# -------------------------------
class QualificationType(models.TextChoices):
    CIVIL = "civil", "Civil"
    OTHER = "other", "Other"