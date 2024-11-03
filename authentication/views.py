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
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email =request.data.get("email")
        password = request.data.get("password")

        # Authenticate the user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Generate a token for the authenticated user
            token, created = Token.objects.get_or_create(user=user)

            # Determine user role by checking existence in respective models
            user_role = None
            user_data = {}

            if User.objects.filter(user=user).exists():
                user_role = "Admin"
                admin = User.objects.get(user=user)
                user_data = {
                    "full_name": admin.user_name,
                    "email": admin.email,
                }
            elif Manager.objects.filter(user=user).exists():
                user_role = "Manager"
                manager = Manager.objects.get(user=user)
                user_data = {
                    "full_name": manager.name,
                    "email": manager.email,
                    "hotel": manager.hotel,
                }
            elif Staff.objects.filter(user=user).exists():
                user_role = "Staff"
                staff = Staff.objects.get(user=user)
                user_data = {
                    "full_name": staff.name,
                    "email": staff.email,
                    "role": staff.role,
                    "sub_role": staff.sub_role,
                    "hotel": staff.hotel,
                }

            # Response with token, role, and role-specific data
            return Response({
                "token": token.key,
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
    
class ResetPassView(UpdateAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = resetPassSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()  
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        
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

