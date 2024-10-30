
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

     return send_mail(subject, message, from_email , recipient_list)


