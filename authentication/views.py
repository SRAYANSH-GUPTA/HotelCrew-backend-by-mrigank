from rest_framework import status, viewsets
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
                "refress_token": str(refresh),
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
    
class OTPVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ManagerViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

    def perform_create(self, serializer):
        serializer.save()  # Calls the `create()` method in the serializer
        return Response({"status": "Manager created and email sent successfully."}) 

class ReceptionistViewSet(viewsets.ModelViewSet):
    queryset = Receptionist.objects.all()
    serializer_class = ReceptionistSerializer

    def perform_create(self, serializer):
        serializer.save()
        return Response({"status": "Receptionist created and email sent successfully."})

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    def perform_create(self, serializer):
        serializer.save()
        return Response({"status": "Staff created and email sent successfully."})

