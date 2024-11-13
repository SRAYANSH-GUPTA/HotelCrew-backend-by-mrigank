from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Attendance(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    attendance = models.BooleanField(default=False)  # False = Absent, True = Present

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.email} - {self.date} - {'Present' if self.attendance else 'Absent'}"
