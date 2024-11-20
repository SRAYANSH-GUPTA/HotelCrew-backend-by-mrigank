from authentication.models import User
from fcm_django.models import FCMDevice
from django.db import models

class DeviceToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField(blank=True,null=True)  # FCM token sent from the Flutter app
    platform = models.CharField(max_length=10, blank=True,null=True)  # e.g., "android" or "ios" or "web"

    def save(self, *args, **kwargs):
        # Register the token with FCM-Django
        FCMDevice.objects.update_or_create(
            user=self.user,
            registration_id=self.token,
            type=self.platform,  # Device type
        )
        super().save(*args, **kwargs)
