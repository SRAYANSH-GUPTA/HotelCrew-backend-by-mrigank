from django.http import JsonResponse
from .models import DeviceToken
from fcm_django.models import FCMDevice
from authentication.models import Staff,User
from firebase_admin.messaging import Message, Notification
from firebase_admin import messaging

def register_device_token(user, device_token):
        
        # Save token
        DeviceToken.objects.create(user=user, token=device_token, platform="android")
       

# def send_notification(user, title, message):
#     print("Sending Notification")
#     print("User:", user.user.email)
#     user = Staff.objects.get(user__email=user.user.email)

#     print("Staff:", user)
#     devices = FCMDevice.objects.filter(user=user.user)  # Retrieve user's devices
#     print("Devices:", devices)
#     response = devices.send_message(
#         title=title,
#         message=message,
        
#     )
#     print("Notification Response:", response)

def send_fcm_notification(user, title, body):
       print("Sending FCM Notification")
       print("User:", user)       
       token = DeviceToken.objects.get(user=user.user).token
       print("Token:", token)
       message = messaging.Message(
           notification=messaging.Notification(
               title=title,
               body=body,
           ),
           token=token,
          
       )
       response = messaging.send(message)

