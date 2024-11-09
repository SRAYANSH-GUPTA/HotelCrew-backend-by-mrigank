from django.db import models
from django.conf import settings

class HotelDetails(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hotel_details')

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

    def __str__(self):
        return f"{self.room_type} - {self.hotel.hotel_name}"
