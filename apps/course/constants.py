from django.db import models

class YesNo(models.TextChoices):
    YES = "yes", "Yes"
    NO = "no", "No"
    
    