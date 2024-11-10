from rest_framework import serializers
from .models import Task, TaskComment

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'completed_at')

    def validate(self, data):
        # Validate assigner role
        if data['assigned_by'].role not in ['Admin', 'Manager']:
            raise serializers.ValidationError("Only Admin and Manager can assign tasks")
        
        # Validate department match
        if data['assigned_to'].department != data['department']:
            raise serializers.ValidationError("Staff member must belong to the assigned department")
        
        return data