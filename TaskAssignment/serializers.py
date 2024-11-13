from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields =[ 'title', 'description', 'created_at', 'updated_at', 'deadline', 'assigned_to', 'department', 'status', 'completed_at']
        read_only_fields = ('created_at', 'updated_at', 'completed_at')

    def validate(self, data):
        # Get the user from the context instead of data
        user = self.context['request'].user
        hotel = self.context.get('hotel')
        # Add assigned_by to data
        data['assigned_by'] = user
       # Check if hotel is provided
        if not hotel:
            raise serializers.ValidationError("Hotel information is required for task assignment.")
        # Validate assigner role
        if data['assigned_by'].role not in [ 'Manager', 'Receptionist']:
            raise serializers.ValidationError("Only Manager and Receptionist can assign tasks")
        
        # Validate department match
        if data['assigned_to'].department != data['department']:
            raise serializers.ValidationError("Staff member must belong to the assigned department")
        
        if data['assigned_to'].hotel != hotel:
            raise serializers.ValidationError("Staff member must belong to the assigned_by hotel")
        
        return data

    def create(self, validated_data):
        hotel = self.context.get('hotel')
        task = Task.objects.create(hotel=hotel, **validated_data)
        return task