from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import *





urlpatterns = [
   path('registrationOTP/', RegistrationOTPView.as_view(), name='register_otp'),
    path('register/', RegisterWithOTPView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forget-password/', ForgetPassword.as_view(), name='forgetpassword'),
  #  path('verify-otp/', OTPVerificationView.as_view(), name='verify-otp'),
    path('reset-password/',ResetPasswordView.as_view(),name='reset-password'),
]