from rest_framework import serializers
from .models import Task, TaskComment, Announcement
from hoteldetails.models import HotelDetails
from authentication.models import User, Manager, Staff, Receptionist

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields =[ 'title', 'description', 'created_at', 'updated_at', 'deadline','department', 'status', 'completed_at']
        read_only_fields = ('created_at', 'updated_at', 'completed_at')

    def validate(self, data):
        # Get the user from the context instead of data
        user = self.context['request'].user
        if(user.role == 'Admin'):
            hotel = HotelDetails.objects.get(user=user)
        elif(user.role == 'Manager'):
            manager = Manager.objects.get(user=user)
            hotel = manager.hotel
        elif(user.role == 'Receptionist'):
            receptionist = Receptionist.objects.get(user=user)
            hotel = receptionist.hotel
        else:
            raise serializers.ValidationError("Only Admin, Manager and Receptionist can assign tasks")
        data['hotel'] = hotel
        # Add assigned_by to data
        data['assigned_by'] = user
       # Check if hotel is provided
        if not hotel:
            raise serializers.ValidationError("Hotel information is required for task assignment.")
        # Validate assigner role
        if data['assigned_by'].role not in [ 'Admin','Manager', 'Receptionist']:
            raise serializers.ValidationError("Only Admin, Manager and Receptionist can assign tasks")
        
        staff = Staff.objects.get(department=data['department'], hotel=hotel)
        data['assigned_to'] = staff

        return data

    def create(self, validated_data):
        task = Task.objects.create( **validated_data)
        return task
    

class AnnouncementSerializer(serializers.ModelSerializer):
    assigned_to = serializers.StringRelatedField(many=True, read_only=True)
    assigned_by = serializers.StringRelatedField(read_only=True)
    hotel = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'description', 'created_at', 'assigned_to',
            'assigned_by', 'department', 'hotel', 'urgency'
        ]

class AnnouncementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = [
            'title', 'description', 'department', 'urgency', 'hotel'
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['assigned_by'] = request.user
        return super().create(validated_data)