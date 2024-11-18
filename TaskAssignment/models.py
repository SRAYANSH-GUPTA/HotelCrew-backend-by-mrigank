from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)
    
    # Task assignment details
    assigned_to = models.ForeignKey('authentication.Staff', on_delete=models.CASCADE, related_name='assigned_tasks')
    assigned_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='created_tasks')
    department = models.CharField(max_length=50)
    hotel = models.ForeignKey('hoteldetails.HotelDetails', on_delete=models.CASCADE, related_name='hotel_tasks')
    
    # Task status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    completed_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        # Validate that the task is assigned to staff in the correct department
        if self.assigned_to.department != self.department:
            raise ValidationError("Task must be assigned to staff in the same department")
        
        # Validate that the assigner is either an Admin or Manager
        if self.assigned_by.role not in ['Admin','Manager', 'Receptionist']:
            raise ValidationError("Tasks can only be assigned by Admin, Manager or Receptionist")

    def save(self, *args, **kwargs):
        # When status is changed to completed, set completion time
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.department} ({self.status})"

class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.task.title} by {self.user.email}"