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

        # Authenticate the user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Generate JWT tokens for the authenticated user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Determine user role by checking existence in respective models
            user_role = None
            user_data = {}

            if User.objects.filter(email=email).exists():
                user_role = user.role
                admin = User.objects.get(email=email)
                user_data = {
                    "full_name": admin.user_name,
                    "email": admin.email,
                }
            elif Manager.objects.filter(email=email).exists():
                user_role = "Manager"
                manager = Manager.objects.get(email=email)
                user_data = {
                    "full_name": manager.name,
                    "email": manager.email,
                    "hotel": manager.hotel,
                }
            elif Staff.objects.filter(email=email).exists():
                user_role = "Staff"
                staff = Staff.objects.get(email=email)
                user_data = {
                    "full_name": staff.name,
                    "email": staff.email,
                    "role": staff.role,
                    "sub_role": staff.sub_role,
                    "hotel": staff.hotel,
                }

            # Response with token, role, and role-specific data
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

