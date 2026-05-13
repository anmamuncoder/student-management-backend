from django.db import models

class ResultStatus(models.TextChoices):
    PASS = "pass", "Pass"
    FAIL = "fail", "Fail"
    INCOMPLETE = "incomplete", "Incomplete"
