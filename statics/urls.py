from django.urls import path
from .views import *

urlpatterns = [
    path('performance/hotel/week/', WeeklyHotelPerformanceView.as_view(), name='hotel-performance-weekly'),
    path('performance/staff/currentweek/', CurrentWeeklyStaffPerformanceView.as_view(), name='staff-performance-monthly'),
    path('finance/week/', WeeklyFinanceView.as_view(), name='finance-monthly'),
    path('performance/hotel/past7/', PastWeeklyHotelPerformanceView.as_view(), name='hotel-performance-weekly'),

]
