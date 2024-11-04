
from django.core.mail import send_mail
from django.conf import settings
from HotelCrew.settings import EMAIL_HOST_USER
                

    
def otp_for_reset(email,otp):
     subject="OTP to Reset Password "
     message = f"""
Your OTP to reset your password is:
{otp}
Do not share your otp with anyone.
-team hotelcrew
""" 
     
     from_email = settings.EMAIL_HOST_USER
     recipient_list = [email]

     return send_mail(subject,message,from_email,recipient_list)

def otp_for_register(user_name,email,otp):
     subject="Your OTP Code for Verification"
     message =  f"""
Hi {user_name},
Thank you for registering with us. To complete your verification, please use the following One-Time Password (OTP):

OTP: {otp}


Please do not share it with anyone for security reasons.

Best regards,
HotelCrew 

""" 
  
     from_email = settings.EMAIL_HOST_USER
     recipient_list = [email]

     return send_mail(subject, message, from_email , recipient_list)