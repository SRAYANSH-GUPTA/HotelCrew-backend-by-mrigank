from datetime import datetime
import pytz
from .models import HotelDetails
from authentication.models import Manager, Receptionist, Staff,User


def get_shift():
        # Get the current time and determine the shift
        timezone = pytz.timezone('Asia/Kolkata')  # Replace with your timezone if needed
        current_time = datetime.now(timezone).time()

        if current_time >= datetime.strptime('06:00', '%H:%M').time() and \
           current_time < datetime.strptime('14:00', '%H:%M').time():
            return 'Morning'
        elif current_time >= datetime.strptime('14:00', '%H:%M').time() and \
             current_time < datetime.strptime('22:00', '%H:%M').time():
            return 'Evening'
        else:
            return 'Night'
    
def get_hotel(user):
    if user.role=='Admin':
        if HotelDetails.objects.filter(user=user).exists():   
           hotel = HotelDetails.objects.get(user=user)
        else:
            hotel = None
    elif user.role=='Manager':
        if Manager.objects.filter(user=user).exists():
           hotel = Manager.objects.get(user =user).hotel
        else:
            hotel = None
    elif user.role=='Receptionist':
        if Receptionist.objects.filter(user=user).exists():
           hotel = Receptionist.objects.get(user=user).hotel
        else:
            hotel = None
    elif user.role=='Staff':
        if Staff.objects.filter(user=user).exists():
           hotel = Staff.objects.get(user=user).hotel
        else:
            hotel = None
    return hotel