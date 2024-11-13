from hoteldetails.models import HotelDetails
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer

class IsManagerOrReceptionist(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['Manager', 'Receptionist']


class Taskassignment(CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsManagerOrReceptionist]
    queryset = Task.objects.all()

    def post(self, request):
         
         if not request.user.is_authenticated:
            return Response({
                'status': 'error',
                'message': 'User must be authenticated.'
            }, status=status.HTTP_403_FORBIDDEN)
            
         user = request.user  
         hotel = getattr(user, 'hotel', None)
         hotel_id = user.hotel.id
         if not hotel_id:
             return Response({
                 'status': 'error',
                 'message': 'Hotel ID is required.'
             }, status=status.HTTP_400_BAD_REQUEST)
         
         try:
            hotel = HotelDetails.objects.get(id=hotel_id)
         except HotelDetails.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Hotel not found.'
            }, status=status.HTTP_404_NOT_FOUND)
         
         serializer = self.get_serializer(data=request.data, context={'request': request, 'hotel':hotel})
         if serializer.is_valid():
             task = serializer.save()
             return Response({
                    'status': 'success',
                    'message': 'Task created successfully',
                    'data': serializer.data
             }, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)