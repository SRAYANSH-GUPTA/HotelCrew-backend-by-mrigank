from django.urls import path
from .views import *

urlpatterns = [
    path('register/', HotelDetailView.as_view(), name='hotelRegister'),

]