from django.urls import path
from .views import *





urlpatterns = [
    path('mark/', MarkAttendanceView.as_view(), name='mark_attendance'),
]