from django.urls import path
from .views import *

urlpatterns = [
    path('list/', AttendanceListView.as_view(), name='list'),
    path('change/<int:user_id>/', ChangeAttendanceView.as_view(), name='mark-attendance'),
    path('check/',CheckAttendanceView.as_view(),name='check-attendance'),
    path('month/',MonthlyAttendanceView.as_view(),name='monthly-attendance'),
    path('stats/',AttendanceStatsView.as_view(),name='attendance-stats'),
    path('week-stats/',AttendanceWeekStatsView.as_view(),name='attendance-weekly-stats'),
    path('apply_leave/',ApplyLeaveView.as_view(),name='apply-leave'),
    path('leave_list/',LeaveRequestListView.as_view(),name='leave-list'),
    path('leave_approve/<int:leave_id>/',ApproveLeaveView.as_view(),name='approve-leave'),
    path('leave_count/',LeaveCountView.as_view(),name='leave-count'),
]