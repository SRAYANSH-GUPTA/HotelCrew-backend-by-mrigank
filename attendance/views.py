from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from authentication.models import User
from .models import Attendance

class MarkAttendanceView(APIView):
    def post(self, request):
        user_ids = request.data.get('user_ids', [])
        if not user_ids:
            return Response({'error': 'No user IDs provided.'}, status=status.HTTP_400_BAD_REQUEST)

        date_today = timezone.now().date()

        for user_id in user_ids:
            try:
                user = User.objects.get(id=user_id)
                if user.role != 'Admin': 
                    attendance, created = Attendance.objects.get_or_create(
                        user=user,
                        date=date_today,
                        defaults={'attendance': True}
                    )
                    if not created:
                        attendance.attendance = True
                        attendance.save()
            except User.DoesNotExist:
                return Response({'error': f'User with ID {user_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Attendance marked as present for specified users.'}, status=status.HTTP_200_OK)
