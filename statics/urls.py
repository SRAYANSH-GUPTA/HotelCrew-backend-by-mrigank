from django.urls import path
from .views import MonthlyHotelPerformanceView, MonthlyStaffPerformanceView

urlpatterns = [
    path('performance/hotel/monthly/', MonthlyHotelPerformanceView.as_view(), name='hotel-performance-monthly'),
    path('performance/staff/monthly/', MonthlyStaffPerformanceView.as_view(), name='staff-performance-monthly'),
]
