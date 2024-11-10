from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        
        # Admin can see all tasks
        if user.role == 'Admin':
            return Task.objects.all()
        
        # Manager can see tasks in their hotel
        elif user.role == 'Manager':
            return Task.objects.filter(hotel=user.manager_profile.hotel)
        
        # Staff can only see their assigned tasks
        elif user.role == 'Staff':
            return Task.objects.filter(assigned_to=user.staff_profile)
        
        return Task.objects.none()

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        task = self.get_object()
        new_status = request.data.get('status')
        
        # Only staff can update status and only to in_progress or completed
        if request.user.role != 'Staff':
            return Response({'error': 'Only staff can update task status'}, status=400)
        
        if new_status not in ['in_progress', 'completed']:
            return Response({'error': 'Invalid status'}, status=400)
        
        task.status = new_status
        task.save()
        return Response({'status': 'updated'})