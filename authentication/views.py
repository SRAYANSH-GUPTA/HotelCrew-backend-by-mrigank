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
from Notification.views import register_device_token

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
                # "user_profile":user.user_profile,
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email =request.data.get("email")
        password = request.data.get("password")
        device_token = request.data.get("device_token")

        user_role = None
        user_data = {}
        user = None

        # Authenticate as a User
        user = authenticate(request, email=email, password=password)
        register_device_token(user, device_token)

        if user is not None:
            user_role = user.role
            user_data = {
                "full_name": user.user_name,
                "email": user.email,
                "role": user.role,

            }
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

