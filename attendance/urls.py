from django.urls import path
from .views import *

urlpatterns = [
    path('list/', AttendanceListView.as_view(), name='list'),
    path('change/<int:user_id>/', ChangeAttendanceView.as_view(), name='mark-attendance'),
    path('check/',CheckAttendanceView.as_view(),name='check-attendance'),
    path('stats/',AttendanceStatsView.as_view(),name='attendance-stats'),
]