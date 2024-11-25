from hoteldetails.models import HotelDetails
from rest_framework import permissions
from rest_framework.generics import CreateAPIView,UpdateAPIView,DestroyAPIView,ListAPIView
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from .models import Task,Announcement
from .serializers import TaskSerializer, AnnouncementSerializer, AnnouncementCreateSerializer
from TaskAssignment.permissions import IsAdminorManagerOrReceptionist
from rest_framework.permissions import AllowAny, IsAuthenticated
from authentication.models import Staff, User, DeviceToken, Manager, Receptionist
from authentication.firebase_utils import send_firebase_notification
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from authentication.throttling import updateTaskThrottle
class ListPagination(PageNumberPagination):
    page_size = 10


class Taskassignment(CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAdminorManagerOrReceptionist]
    queryset = Task.objects.all()

    def post(self, request):
         
         if not request.user.is_authenticated:
            return Response({
                'status': 'error',
                'message': 'User must be authenticated.'
            }, status=status.HTTP_403_FORBIDDEN)
            
   
         
         serializer = self.get_serializer(data=request.data, context={'request': request})
         if serializer.is_valid():
             task = serializer.save()
             user = Staff.objects.get(id=task.assigned_to.id).user
             token = DeviceToken.objects.get(user= user).fcm_token
             send_firebase_notification(fcm_token=token, title=task.title, body=task.description)
             Staff.objects.filter(id=task.assigned_to.id).update(is_avaliable=False)
             return Response({
                    'status': 'success',
                    'message': 'Task created successfully',
                    # 'assigned_by': task.assigned_by,
                    # 'assigned_to': task.assigned_to,
                    'data': serializer.data,
             }, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffTaskListView(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    pagination_class = ListPagination

    def get_queryset(self):
        user= self.request.user
        user = user.id
        return Task.objects.filter(assigned_to=user)
    

class AllTaskListView(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAdminorManagerOrReceptionist]
    queryset = Task.objects.all()
    pagination_class = ListPagination

    def get_queryset(self):
        return Task.objects.all()
    

class TaskUpdateView(UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAdminorManagerOrReceptionist]
    throttle_classes = [updateTaskThrottle]
    queryset = Task.objects.all()
    lookup_field = 'pk'


class TaskDeleteView(DestroyAPIView):
    permission_classes = [IsAdminorManagerOrReceptionist]
    queryset = Task.objects.all()
    lookup_field = 'pk'


class TaskStatusUpdateView(APIView):
    permission_classes=[AllowAny]
    throttle_classes = [updateTaskThrottle]
    def patch(self, request, pk=None):
        """
        Allows to update only the status field of a task.
        """
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        # Only allow updating the status field
        status_data = request.data.get("status")
    
        if status_data is not None:
            if status_data == "Completed":
                task.completed_at = timezone.now()
                Staff.objects.filter(id=task.assigned_to.id).update(is_available=True)
            task.status = status_data
            task.save()
            return Response({
                "message": "Task status updated successfully",
                "status": task.status
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Status field is required"}, status=status.HTTP_400_BAD_REQUEST)


class AnnouncementListCreateView(APIView):
    """
    Handles listing all announcements and creating new ones.
    """
    permission_classes = [permissions.IsAuthenticated]
    

    def get(self, request):
        """
        List all announcements.
        Admin and managers see all announcements, staff see only assigned ones.
        """
        user = request.user
        if user.role == 'Manager':
            user = Manager.objects.get(user=user)
            announcements = Announcement.objects.filter(hotel=user.hotel)
        elif user.role == 'receptionist':
            user = Receptionist.objects.get(user=user)
            announcements = Announcement.objects.filter(hotel=user.hotel)
        elif user.role == 'Admin':
            hotel = HotelDetails.objects.get(user = user)
            announcements = Announcement.objects.filter(hotel=hotel)
        else:
            announcements = Announcement.objects.filter(assigned_to= user)
        
        paginator = PageNumberPagination()
        paginator.page_size = 10 
        paginated_announcements = paginator.paginate_queryset(announcements, request)
        serializer = AnnouncementSerializer(paginated_announcements, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Create a new announcement.
        Only admin and managers can create announcements.
        """
        if not (request.user.role == 'Admin' or request.user.role == 'Manager'):
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AnnouncementCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # serializer.save(assigned_by=request.user)

            # if serializer.data['department'] == 'All':
            #     user = Staff.objects.all()
            # else:
            #     user = Staff.objects.all(department=serializer.data['department'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnnouncementDetailView(APIView):
    """
    Handles retrieving and deleting a specific announcement.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        """
        Retrieve the announcement object or return a 404 error.
        """
        try:
            return Announcement.objects.get(pk=pk)
        except Announcement.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Retrieve a specific announcement.
        """
        announcement = self.get_object(pk)
        if announcement is None:
            return Response({"error": "Announcement not found."}, status=status.HTTP_404_NOT_FOUND)

        if not (request.user.is_admin or request.user.is_manager or announcement.assigned_to.filter(id=request.user.staff.id).exists()):
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AnnouncementSerializer(announcement)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """
        Delete a specific announcement.
        """
        announcement = self.get_object(pk)
        if announcement is None:
            return Response({"error": "Announcement not found."}, status=status.HTTP_404_NOT_FOUND)

        if not (request.user.role == 'Admin' or request.user.role == 'Manager'):
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        announcement.delete()
        return Response({"message": "Announcement deleted successfully."}, status=status.HTTP_204_NO_CONTENT)  
        