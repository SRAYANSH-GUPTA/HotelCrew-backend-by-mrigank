from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from attendance.models import *
from .serializers import MonthlyHotelPerformanceSerializer, MonthlyStaffPerformanceSerializer
from datetime import timedelta
from django.utils.timezone import now
from attendance.permissions import *
from TaskAssignment.models import Task
from authentication.models import Staff

class MonthlyHotelPerformanceView(APIView):
    permission_classes = [IsManagerOrAdmin]

    def get(self, request):
        user = request.user
        if user.role not in ['Admin', 'Manager']:
            return Response({"error": "You do not have permission to view this data."}, status=status.HTTP_403_FORBIDDEN)

        today = now().date()
        first_day = today.replace(day=1)
        last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        daily_stats = []
        for single_date in (first_day + timedelta(days=x) for x in range((last_day - first_day).days + 1)):
            staff_present = Attendance.objects.filter(date=single_date, attendance = True).count()
            staff_on_leave = Leave.LeaveCount(single_date)
            tasks_completed = Task.objects.filter(status='Completed', created_at=single_date).count()
            tasks_assigned = Task.objects.filter(created_at=single_date).count()

            performance_percentage = (
                ((staff_present / (staff_present + staff_on_leave)) if (staff_present + staff_on_leave) > 0 else 0)
                + (tasks_completed / tasks_assigned if tasks_assigned > 0 else 0)
            ) / 2 * 100

            daily_stats.append({
                'date': single_date,
                'performance_percentage': performance_percentage
            })

        data = {
            'month': today.strftime('%B %Y'),
            'daily_stats': daily_stats
        }
        serializer = MonthlyHotelPerformanceSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MonthlyStaffPerformanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user1 = request.user
        if user1.role != 'Staff':
            return Response({"error": "You do not have permission to view this data."}, status=status.HTTP_403_FORBIDDEN)
        
        user2 = Staff.objects.get(user=user1)

        today = now().date()
        first_day = today.replace(day=1)
        last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        daily_stats = []

        for single_date in (first_day + timedelta(days=x) for x in range((last_day - first_day).days + 1)):

            attendance = Attendance.objects.filter(user=user1, date=single_date).first()  

            tasks_completed = Task.objects.filter(assigned_to=user2, status='Completed', created_at__date=single_date).count()
            tasks_assigned = Task.objects.filter(assigned_to=user2, created_at__date=single_date).count()

            presence_status = 'Present' if attendance and attendance.attendance else 'Leave' if Leave.objects.filter(
                user=user1, from_date__lte=single_date, to_date__gte=single_date, status='Approved').exists() else 'Absent'
            
            performance_percentage = (
                (1 if presence_status == 'Present' else 0.5 if presence_status == 'Leave' else 0)
                + (tasks_completed / tasks_assigned if tasks_assigned > 0 else 0)
            ) * 50

            daily_stats.append({
                'date': single_date,
                'performance_percentage': performance_percentage
            })

        data = {
            'month': today.strftime('%B %Y'),
            'daily_stats': daily_stats
        }
        serializer = MonthlyStaffPerformanceSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
