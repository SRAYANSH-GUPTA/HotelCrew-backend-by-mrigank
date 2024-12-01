from django.contrib import admin
from .models import HotelDetails,RoomType,Customer


class HotelDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','hotel_name', 'email_address')
    search_fields = ('hotel_name', 'email_address')
    ordering = ('hotel_name',)

class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'hotel', 'room_type', 'count', 'price')
    search_fields = ('hotel', 'room_type')
    ordering = ('hotel',)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'hotel', 'check_in_time', 'check_out_time', 'name', 'phone_number', 'email', 'room')
    search_fields = ('hotel', 'name', 'phone_number', 'email', 'room')
    ordering = ('hotel',)
admin.site.register(HotelDetails, HotelDetailsAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Customer, CustomerAdmin)
