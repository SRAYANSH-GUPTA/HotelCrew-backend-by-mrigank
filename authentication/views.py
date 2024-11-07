from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import *
from django.http import JsonResponse
from rest_framework.generics import *
from .models import *

def home_view(request):
    return JsonResponse({"message": "Welcome to the HotelCrew!"})


class RegistrationOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationOTPSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterWithOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterWithOTPSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({
                "message": "User registered successfully",
                 "access_token": access_token,
                "refresh_token": str(refresh),
                "user_id": user.id,
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email =request.data.get("email")
        password = request.data.get("password")

        user_role = None
        user_data = {}
        user = None

        # Authenticate as a User (Admin)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            user_role = user.role
            user_data = {
                "full_name": user.user_name,
                "email": user.email,
            }
        
        # Authenticate as a Manager
        elif Manager.objects.filter(email=email, password=password).exists():
            manager = Manager.objects.get(email=email)
            user_role = "Manager"
            user_data = {
                "full_name": manager.name,
                "email": manager.email,
                "hotel": manager.hotel.id,  # Assuming you want hotel ID
            }
            # Creating a dummy user for token generation
            user = User(email=manager.email, user_name=manager.name)

        # Authenticate as a Receptionist
        elif Receptionist.objects.filter(email=email, password=password).exists():
            receptionist = Receptionist.objects.get(email=email)
            user_role = "Receptionist"
            user_data = {
                "full_name": receptionist.name,
                "email": receptionist.email,
                "hotel": receptionist.hotel.id,
            }
            user = User(email=receptionist.email, user_name=receptionist.name)

        # Authenticate as Staff
        elif Staff.objects.filter(email=email, password=password).exists():
            staff = Staff.objects.get(email=email)
            user_role = "Staff"
            user_data = {
                "full_name": staff.name,
                "email": staff.email,
                "role": staff.role,
                "sub_role": staff.sub_role,
                "hotel": staff.hotel.id,
            }
            user = User(email=staff.email, user_name=staff.name)

        # If a valid role was identified, create JWT tokens
        if user_role:
            # Generate JWT tokens (use a dummy User instance for token generation)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                
                "access_token": access_token,
                "refress_token": str(refresh),
                "role": user_role,
                "user_data": user_data
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
class ForgetPassword(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = ForgetPassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message' : ['OTP sent on email']}, status=status.HTTP_200_OK)
    
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'Admin'

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

class ReceptionistViewSet(viewsets.ModelViewSet):
    queryset = Receptionist.objects.all()
    serializer_class = ReceptionistSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

class EmailOTPViewSet(viewsets.ModelViewSet):

    queryset = EmailOTP.objects.all()
    serializer_class = EmailOTPSerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'])
    def generate_otp(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        email_otp, created = EmailOTP.objects.update_or_create(
            email=email,
            defaults={'otp': otp, 'otp_verified': False}
        )
        
        # Send OTP email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is: {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        
        return Response({'message': 'OTP sent successfully'})
    
    @action(detail=False, methods=['post'])
    def verify_otp(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        
        try:
            email_otp = EmailOTP.objects.get(email=email)
            if email_otp.is_otp_expired():
                return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)
            
            if email_otp.otp == otp:
                email_otp.otp_verified = True
                email_otp.save()
                return Response({'message': 'OTP verified successfully'})
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        except EmailOTP.DoesNotExist:
            return Response({'error': 'No OTP found for this email'}, status=status.HTTP_404_NOT_FOUND)
        """