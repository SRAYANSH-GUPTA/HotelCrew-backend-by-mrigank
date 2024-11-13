from rest_framework import serializers
from authentication.models import User
from .models import Attendance
from django.utils import timezone

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['date', 'attendance']
        
class UserWithAttendanceSerializer(serializers.ModelSerializer):
    current_attendance = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'current_attendance']

    def get_current_attendance(self, obj):
        today = timezone.now().date()
        attendance = Attendance.objects.filter(user=obj, date=today).first()
        return 'Present' if attendance and attendance.attendance else 'Absent'
