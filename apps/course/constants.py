from django.db import models

class YesNo(models.TextChoices):
    YES = "yes", "Yes"
    NO = "no", "No"
    
class SubjectMethod(models.TextChoices):
    PRACTICAL = "PRACTICAL", "Practical"
    LECTURAL = "LECTURAL", "Lectural"
    WRITTEN = "WRITTEN", "Written"
    OTHER = "OTHER", "Other"