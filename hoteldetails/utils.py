from datetime import datetime
import pytz
from .models import HotelDetails
from authentication.models import Manager, Receptionist, Staff,User


def get_shift():
        # Get the current time and determine the shift
        timezone = pytz.timezone('Asia/Kolkata')  # Replace with your timezone if needed
        current_time = datetime.now(timezone).time()

        if current_time >= datetime.strptime('00:00', '%H:%M').time() and \
           current_time < datetime.strptime('08:00', '%H:%M').time():
            return 'Morning'
        elif current_time >= datetime.strptime('08:00', '%H:%M').time() and \
             current_time < datetime.strptime('16:00', '%H:%M').time():
            return 'Evening'
        else:
            return 'Night'
    
def get_hotel(user):
    if user.role=='Admin':
        hotel = HotelDetails.objects.get(user=user)
    elif user.role=='Manager':
        hotel = Manager.objects.get(user =user).hotel
    elif user.role=='Receptionist':
        hotel = Receptionist.objects.get(user=user).hotel
    elif user.role=='Staff':
        hotel = Staff.objects.get(user=user).hotel
    return hotel