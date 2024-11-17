from django.urls import path
from .views import *

urlpatterns = [
    path('list/', StaffListView.as_view(), name='staff-list'),
    path('create/',CreateCrewView.as_view(),name='staff-create'),
    path('update/<int:user_id>/',UpdateCrewView.as_view(),name='staff-update'),
    path('delete/<int:user_id>/',DeleteCrewView.as_view(),name='staff-delete'),
    path('hoteldetails/',UpdateHotelDetailsView.as_view(),name='hotel-update'),
]