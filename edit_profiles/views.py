from itertools import chain
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions

from authentication.models import User,Manager,Receptionist,Staff
from hoteldetails.models import HotelDetails

from .serializers import StaffListSerializer,UserSerializer

# Create your views here.

class IsManagerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['Manager', 'Admin']

class StaffListView(ListAPIView):
     permission_classes = [IsManagerOrAdmin]

     def get(self, request):
        
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
        
        serializer = StaffListSerializer(non_admin_users, many=True)
        return Response(serializer.data, status=200)
    

class CreateCrewView(APIView):
    permission_classes = [IsManagerOrAdmin]

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'status': 'error', 'message': 'User must be authenticated.'}, status=status.HTTP_403_FORBIDDEN)
        
        

        try:
            user_hotel = HotelDetails.objects.get(user=request.user)
        except HotelDetails.DoesNotExist:
            return Response({'status': 'error', 'message': 'No hotel is associated with the authenticated user.'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        role = data.get('role', 'Staff').capitalize()
        email, user_name = data.get('email'), data.get('user_name')
        department = data.get('department')

        if not email:
            return Response({'status': 'error', 'message': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        valid_roles = dict(User.ROLE_CHOICES).keys()
        if role not in valid_roles:
            return Response({'status': 'error', 'message':'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)


        try:
            user = User.objects.create_user(email=email, user_name=user_name, role=role)

            if role.lower() == 'manager':
                Manager.objects.create(user=user, hotel=user_hotel)
            elif role.lower() == 'receptionist':
                Receptionist.objects.create(user=user, hotel=user_hotel)
            else:
                Staff.objects.create(user=user, hotel=user_hotel, department=department)

        except Exception as e:
            return Response({'status': 'error', 'message': f"Error creating user: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user)
        return Response({'status': 'success', 'message': 'User created successfully.', 'user': serializer.data}, status=status.HTTP_201_CREATED)
    
class UpdateCrewView(APIView):
    permission_classes = [IsManagerOrAdmin]

    def put(self, request, user_id):
        if not request.user.is_authenticated:
            return Response({'status': 'error', 'message': 'User must be authenticated.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'status': 'error', 'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            user_hotel = HotelDetails.objects.get(user=request.user)
        except HotelDetails.DoesNotExist:
            return Response({'status': 'error', 'message': 'No hotel is associated with the authenticated user.'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        new_role = data.get('role', user.role).capitalize()
        new_email = data.get('email', user.email)
        user_name = data.get('user_name', user.user_name)
        department = data.get('department')

        if new_email != user.email:
            try:
                validate_email(new_email)
            except ValidationError:
                return Response({'status': 'error', 'message': 'Invalid email format.'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=new_email).exists():
                return Response({'status': 'error', 'message': 'This email is already in use.'}, status=status.HTTP_400_BAD_REQUEST)

            user.email = new_email


        valid_roles = dict(User.ROLE_CHOICES).keys()
        if new_role not in valid_roles:
            return Response({'status': 'error', 'message': f'Invalid role. Choose from {", ".join(valid_roles)}.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if new_role != user.role:

            if user.role == 'Manager':
                Manager.objects.filter(user=user).delete()
            elif user.role == 'Receptionist':
                Receptionist.objects.filter(user=user).delete()
            elif user.role == 'Staff':
                Staff.objects.filter(user=user).delete()

            if new_role == 'Manager':
                Manager.objects.create(user=user, hotel=user_hotel)
            elif new_role == 'Receptionist':
                Receptionist.objects.create(user=user, hotel=user_hotel)
            elif new_role == 'Staff':
                Staff.objects.create(user=user, hotel=user_hotel, department=department)

        user.user_name = user_name
        user.role = new_role

        try:
            user.save()
        except Exception as e:
            return Response({'status': 'error', 'message': f"Error updating user: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user)
        return Response({'status': 'success', 'message': 'User updated successfully.', 'user': serializer.data}, status=status.HTTP_200_OK)
    
class DeleteCrewView(APIView):
    permission_classes = [IsManagerOrAdmin]

    def delete(self, request, user_id):
        if not request.user.is_authenticated:
            return Response({
                'status': 'error',
                'message': 'You are not allowed to do this operation.'
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            user_to_delete = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'status': 'error', 'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user_to_delete.role == 'Manager':
            Manager.objects.filter(user=user_to_delete).delete()
        elif user_to_delete.role == 'Receptionist':
            Receptionist.objects.filter(user=user_to_delete).delete()
        elif user_to_delete.role == 'Staff':
            Staff.objects.filter(user=user_to_delete).delete()

        user_to_delete.delete()

        return Response({
            'status': 'success',
            'message': 'User and associated data deleted successfully.'
        }, status=status.HTTP_204_NO_CONTENT)
