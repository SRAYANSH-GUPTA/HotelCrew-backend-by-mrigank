from rest_framework import serializers
from authentication.models import User
from .models import Attendance
from django.utils import timezone

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['date', 'attendance']
        
class AttendanceListSerializer(serializers.ModelSerializer):
    current_attendance = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'user_name', 'role','department','current_attendance']

    def get_current_attendance(self, obj):
        today = timezone.now().date()
        attendance = Attendance.objects.filter(user=obj, date=today).first()
        return 'Present' if attendance and attendance.attendance else 'Absent'
    
    def get_department(self, obj):
        if obj.role == 'Staff':
            try:
                return obj.staff_profile.department
            except Staff.DoesNotExist:
                return None
        return obj.role
