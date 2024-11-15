from django.contrib import admin
from .models import HotelDetails,RoomType


class HotelDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','hotel_name', 'email_address')
    search_fields = ('hotel_name', 'email_address')
    ordering = ('hotel_name',)

admin.site.register(HotelDetails, HotelDetailsAdmin)
admin.site.register(RoomType)