from rest_framework import serializers
from authentication.models import User

from django.utils import timezone

        
class StaffListSerializer(serializers.ModelSerializer):
    
    department = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'user_name','email', 'role','department']

    def get_department(self, obj):
        # Check if the user's role is Staff
        if obj.role == 'Staff':
            try:
                # Return the related Staff model's department
                return obj.staff_profile.department
            except Staff.DoesNotExist:
                return None
        return None
    
class UserSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    department = serializers.CharField(required=False, allow_blank=True)  # Relevant for staff only

    class Meta:
        model = User
        fields = ['id', 'user_name', 'email', 'role', 'department']