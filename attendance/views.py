from itertools import chain
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.utils import timezone
from authentication.models import User,Manager,Receptionist,Staff
from hoteldetails.models import HotelDetails
from .models import Attendance
from .serializers import AttendanceListSerializer

class IsManagerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['Manager', 'Admin']

class AttendanceListView(ListAPIView):
     permission_classes = [IsManagerOrAdmin]

     def get(self, request):
        today = timezone.now().date()
        # user_hotel
        
        try:
          
            user_hotel = HotelDetails.objects.filter(user=request.user)
            # print("hi")
        except HotelDetails.DoesNotExist:
            return Response(
                {'error': 'No hotel is associated with you!.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # non_admin_users = User.objects.exclude(role='Admin').filter(hotel=user_hotel)
        managers=Manager.objects.filter(hotel__in=user_hotel)
        staffs=Staff.objects.filter(hotel__in=user_hotel)
        receptionists=Receptionist.objects.filter(hotel__in=user_hotel)
        
        non_admin_users = list(chain(
            (manager.user for manager in managers),
            (staff.user for staff in staffs),
            (receptionist.user for receptionist in receptionists)
        ))
        
        if not Attendance.objects.filter(date=today,user__in=non_admin_users).exists():
            
            # non_admin_users = User.objects.exclude(role='Admin').filter(hotel=user_hotel)

            Attendance.objects.bulk_create([
                Attendance(user=user, date=today, attendance=False) 
                for user in non_admin_users
            ])
            
        serializer = AttendanceListSerializer(non_admin_users, many=True, context={'date': today})
        return Response(serializer.data, status=200)

class ChangeAttendanceView(APIView):
    permission_classes = [IsManagerOrAdmin]
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


class CheckAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        
        today = timezone.now().date()

        try:
            attendance = Attendance.objects.get(user=user, date=today)
            
            attendance_status = "Present" if attendance.attendance else "Absent"
            
            return Response({'date': today,'user': user.user_name,'attendance':
            attendance_status,},
                status=status.HTTP_200_OK
            )
        except Attendance.DoesNotExist:
            return Response({'message': 'No attendance record found for today',},
                status=status.HTTP_200_OK
            )
            
class AttendanceStatsView(APIView):
    permission_classes = [IsManagerOrAdmin]

    def get(self, request):
        today = timezone.now().date()
        
        try:
          
            user_hotel = HotelDetails.objects.filter(user=request.user)
        except HotelDetails.DoesNotExist:
            return Response(
                {'error': 'No hotel is associated with you!.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        managers=Manager.objects.filter(hotel__in=user_hotel)
        staffs=Staff.objects.filter(hotel__in=user_hotel)
        receptionists=Receptionist.objects.filter(hotel__in=user_hotel)
        
        non_admin_users = list(chain(
            (manager.user for manager in managers),
            (staff.user for staff in staffs),
            (receptionist.user for receptionist in receptionists)
        ))
        
        present = Attendance.objects.filter(
            user__in=non_admin_users,
            date=today,
            attendance=True
        )
        crew = Attendance.objects.filter(
            user__in=non_admin_users,
            date=today,
        )
        total_present=present.count()
        total_crew=crew.count()
        return Response({
            'total_crew': total_crew,
            'total_present': total_present
        }, status=status.HTTP_200_OK)

