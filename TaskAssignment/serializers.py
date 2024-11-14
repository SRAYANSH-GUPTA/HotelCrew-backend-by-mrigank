from rest_framework import serializers
from .models import Task
from hoteldetails.models import HotelDetails
from authentication.models import User, Manager, Staff

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields =[ 'title', 'description', 'created_at', 'updated_at', 'deadline','department', 'status', 'completed_at']
        read_only_fields = ('created_at', 'updated_at', 'completed_at')

    def validate(self, data):
        # Get the user from the context instead of data
        user = self.context['request'].user
        manager = Manager.objects.get(user=user)
        hotel = manager.hotel
        data['hotel'] = hotel
        # Add assigned_by to data
        data['assigned_by'] = user
       # Check if hotel is provided
        if not hotel:
            raise serializers.ValidationError("Hotel information is required for task assignment.")
        # Validate assigner role
        if data['assigned_by'].role not in [ 'Manager', 'Receptionist']:
            raise serializers.ValidationError("Only Manager and Receptionist can assign tasks")
        
        staff = Staff.objects.get(department=data['department'], hotel=hotel)
        data['assigned_to'] = staff

        return data

    def create(self, validated_data):
        task = Task.objects.create( **validated_data)
        return task