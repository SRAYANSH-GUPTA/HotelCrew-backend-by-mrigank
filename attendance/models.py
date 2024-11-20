from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Attendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    attendance = models.BooleanField(default=False)  # False = Absent, True = Present

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.email} - {self.date} - {'Present' if self.attendance else 'Absent'}"

class Leave(models.Model):
    LEAVE_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leave_request')
    from_date = models.DateField()
    to_date = models.DateField()
    leave_type = models.CharField(max_length=50, blank=False,null=False)
    status = models.CharField(max_length=10, choices=LEAVE_STATUS_CHOICES, default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Leave Request for {self.user} ({self.status})"

    def LeaveCount(date):
        
        return Leave.objects.filter(
            status='Approved',
            from_date__lte=date,
            to_date__gte=date
        ).count()




