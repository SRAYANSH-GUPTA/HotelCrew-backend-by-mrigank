from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *


router = DefaultRouter()
router.register(r'staffs', StaffViewSet)
router.register(r'managers', ManagerViewSet)
router.register(r'receptionists', ReceptionistViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('registrationOTP/', RegistrationOTPView.as_view(), name='register_otp'),
    path('register/', RegisterWithOTPView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgetpassword/', ForgetPassword.as_view(), name='forgetpassword'),
    path('resetpassword/', ResetPassView.as_view(), name='resetpassword'),
]