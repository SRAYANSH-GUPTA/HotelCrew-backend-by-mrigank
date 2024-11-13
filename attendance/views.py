from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from django.utils import timezone
from authentication.models import User
from .models import Attendance
from .serializers import UserWithAttendanceSerializer

class NonAdminUserListView(ListAPIView):
    queryset = User.objects.exclude(role='Admin')
    serializer_class = UserWithAttendanceSerializer

class ChangeAttendanceView(APIView):
    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            if user.role == 'Admin':
                return Response({'error': 'Admins cannot have attendance records.'}, status=status.HTTP_400_BAD_REQUEST)

            date_today = timezone.now().date()
            attendance, created = Attendance.objects.get_or_create(
                user=user,
                date=date_today
            )
            
            attendance.attendance = not attendance.attendance
            attendance.save()
            
            return Response(
                {
                    'message': f'Attendance for {user.user_name} on {date_today} set to {"Present" if attendance.attendance else "Absent"}.',
                    'attendance': attendance.attendance
                },
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
