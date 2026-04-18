from django.db import models
from apps.course.models import Course, Batch
from kernel.models import BaseModel

# -------------------------
# Govt Holidays Model
# -------------------------
class GovtHoliday(BaseModel):
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def total_days(self):
        if self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 1

 
# -------------------------
# Training Schedule Model
# -------------------------
class TrainingSchedule(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()

    total_week = models.PositiveIntegerField(blank=True, null=True)
    total_weekend = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.course.name} - {self.batch.name}"

    def save(self, *args, **kwargs):
        # Auto-calculate weeks & weekends
        if self.start_date and self.end_date:
            delta_days = (self.end_date - self.start_date).days + 1

            self.total_week = delta_days // 7

            # Count weekends (Saturday + Sunday)
            weekends = 0
            for i in range(delta_days):
                day = (self.start_date.weekday() + i) % 7
                if day in [5, 6]:  # Saturday, Sunday
                    weekends += 1

            self.total_weekend = weekends

        super().save(*args, **kwargs)

        