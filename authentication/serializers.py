from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework.response import Response
from django.core.validators import MinLengthValidator
from .utils import *
import random
from .models import EmailOTP, User
from django.core.exceptions import ValidationError

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','user_name', 'email')

class RegistrationOTPSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return data

    def save(self):
        email = self.validated_data['email']
        user_name = self.validated_data['user_name']
        password = self.validated_data['password']
   
        otp = random.randint(1000, 9999)

        otp_for_register(user_name,email,otp)
        EmailOTP.objects.update_or_create(email=email, defaults={'otp': otp, 'user_name': user_name, 'password': password})
        
        return {'message': 'OTP sent successfully'}

class RegisterWithOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()
    
    def validate(self, data):
       
        try:
            otp_record = EmailOTP.objects.get(email=data['email'])
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError({'error': 'OTP not found or invalid user'})

        if otp_record.otp != data['otp']:
            raise serializers.ValidationError({'error': 'Invalid OTP'})

        if otp_record.is_otp_expired():
            raise serializers.ValidationError({'error': 'OTP expired'})
        

        return data

    def save(self, **kwargs):
        email = self.validated_data['email']
        otp_record = EmailOTP.objects.get(email=email)
        user_name = otp_record.user_name
        password = otp_record.password

        user = User.objects.create_user(
            email=email,
            user_name=user_name,
            password=password
        )

        otp_record.delete()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ForgetPassSerializer(serializers.Serializer):
     email = serializers.EmailField(write_only=True)

     def validate(self, data):
       user= User.objects.filter(email=data['email']).exists()
       if not user:
           raise serializers.ValidationError({"error":"User doesn't exist"})
       otpto= self.sendotp(data)
       EmailOTP.objects.update_or_create(
            email= data['email'],
            defaults={'otp':otpto,'forgot' :True}
        )
       return data
        
     def sendotp(self, attrs):
        otpto = random.randint(1000, 9999)
        otp_for_reset(attrs['email'], otpto)
        
        return otpto
     

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()

    def validate(self, data):
        try:
            otp_record = EmailOTP.objects.get(email=data['email'], forgot=True)
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError({'error': 'OTP not found or invalid user'})

        if otp_record.otp != data['otp']:
            raise serializers.ValidationError({'error': 'Invalid OTP'})
        if otp_record.is_otp_expired():
            raise serializers.ValidationError({'error': 'OTP expired'})

        data['otp_record'] = otp_record
        return data

    def save(self):
        otp_record = self.validated_data['otp_record']
        otp_record.otp_verified = True 
        otp_record.save()
        return {'message': 'OTP verified successfully'}


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        try:
            otp_record = EmailOTP.objects.get(email=data['email'], otp_verified=True)
            user = User.objects.get(email=data['email'])
        except (EmailOTP.DoesNotExist, User.DoesNotExist):
            raise serializers.ValidationError({"error": "OTP verification required or user does not exist."})

        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        
        
        EmailOTP.objects.filter(email=self.validated_data['email']).delete()  

        return {'message': 'Password reset successfully'}
