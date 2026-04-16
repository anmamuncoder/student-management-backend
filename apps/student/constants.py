from django.db import models

# -------------------------------
# Qualification Type
# -------------------------------
class QualificationType(models.TextChoices):
    CIVIL = "civil", "Civil"
    OTHER = "other", "Other"