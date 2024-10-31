from rest_framework import serializers,status
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework.response import Response
from django.core.validators import MinLengthValidator
from .utils import *
import random
from .models import EmailOTP, User

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','user_name', 'email')

class RegistrationOTPSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return email

    def save(self):
        email = self.validated_data['email']
        user_name = self.validated_data['user_name']
        otp = random.randint(1000, 9999)

        otp_for_register(email, otp)  
        EmailOTP.objects.update_or_create(email=email, defaults={'otp': otp, 'user_name': user_name})
        return {'message': 'OTP sent successfully'}

class RegisterWithOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        # Check if OTP exists and is correct
        try:
            otp_record = EmailOTP.objects.get(email=data['email'])
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError({'error': 'OTP not found or invalid user'})

        if otp_record.otp != data['otp']:
            raise serializers.ValidationError({'error': 'Invalid OTP'})

        # Verify that password and confirm_password match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        return data

    def save(self, **kwargs):
        validated_data = self.validated_data
        email = validated_data['email']
        password = validated_data['password']
        
        # Create the user
        user = User.objects.create_user(
            email=email,
            user_name=EmailOTP.objects.get(email=email).user_name,
            password=password
        )

        # Delete OTP record after successful registration
        EmailOTP.objects.filter(email=email).delete()

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
     

class resetPassSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()
    new_password = serializers.CharField(min_length=8)
    confirm_password = serializers.CharField(min_length=8)

    def validate(self, data):
        try:
            otp_record = EmailOTP.objects.get(email=data['email'])
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError({'error': 'Invalid user or OTP not found'})

        if otp_record.otp != data['otp']:
            raise serializers.ValidationError({'error': 'Invalid OTP'})
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "User with this email does not exist."})

        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        EmailOTP.objects.filter(email=self.validated_data['email']).delete()

        return user