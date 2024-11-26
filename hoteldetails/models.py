from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class HotelDetails(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,unique=True, on_delete=models.CASCADE, related_name='hotel_details')

    # Basic Hotel Information
    hotel_name = models.CharField(max_length=255)
    legal_business_name = models.CharField(max_length=255)
    year_established = models.IntegerField()
    license_registration_numbers = models.CharField(max_length=255)

    # Contact Information
    complete_address = models.TextField()
    main_phone_number = models.CharField(max_length=10)
    emergency_phone_number = models.CharField(max_length=10)
    email_address = models.EmailField()

    # Property Details
    total_number_of_rooms = models.PositiveIntegerField()
    number_of_floors = models.PositiveIntegerField()
    valet_parking_available = models.BooleanField(default=False)
    valet_parking_capacity = models.PositiveIntegerField(blank=True, null=True)

    # Operational Information
    check_in_time = models.TimeField()
    check_out_time = models.TimeField()
    payment_methods = models.TextField(help_text="List accepted payment methods")
    room_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Staff Management
    number_of_departments = models.PositiveIntegerField()
    department_names = models.TextField(help_text="Comma-separated list of department names")

   # Excel Sheet Upload for Staff Creation



    def __str__(self):
        return self.hotel_name


class RoomType(models.Model):
    hotel = models.ForeignKey(HotelDetails, on_delete=models.CASCADE, related_name='room_types')
    room_type = models.CharField(max_length=50)
    count = models.PositiveIntegerField()
    price = models.DecimalField(default=0,max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.room_type} - {self.hotel.hotel_name}"
    
    
class Customer(models.Model):
    hotel = models.ForeignKey(HotelDetails, on_delete=models.CASCADE, related_name='customers')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField()
    room = models.ForeignKey('RoomType', on_delete=models.CASCADE)
    room_no = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    checked_out = models.BooleanField(default=False) 
    status=models.CharField(max_length=10,default="Regular")
    # room_released = models.BooleanField(default=False)  # Track if the room has been released

    # def save(self, *args, **kwargs):
    #     # Automatically release room after checkout time
    #     if not self.room_released and timezone.now() >= self.check_out_time:
    #         self.release_room()
    #     super().save(*args, **kwargs)

    # def release_room(self):
    #     # Update the room count when checkout time has passed
    #     self.room.count += 1
    #     self.room.save()
    #     self.room_released = True
    def __str__(self):
        return f"Customer: {self.name} - Room: {self.room_no}"