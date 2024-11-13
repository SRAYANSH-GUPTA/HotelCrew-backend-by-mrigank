from django.urls import path
from .views import *

urlpatterns = [
    path('list/', NonAdminUserListView.as_view(), name='list'),
    path('change/<int:user_id>/', ChangeAttendanceView.as_view(), name='mark attendance')
]