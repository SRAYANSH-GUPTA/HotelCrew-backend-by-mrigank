from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from datetime import timedelta

class CustomUserManager(BaseUserManager):
    def create_user(self, email, user_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not user_name:
            raise ValueError('Username is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email,  user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, user_name, password, **extra_fields)

class User(AbstractUser):
    username = None 
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=150, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class EmailOTP(models.Model):
    
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True )
    otp = models.IntegerField(null=True, blank=True)
    otp_created_at = models.DateTimeField(auto_now=True)
    user_name = models.CharField(max_length=150)  
    password = models.CharField(max_length=128)   
    forgot=models.BooleanField(default= False, blank= True)
    def __str__(self):
        return f"{self.email} - OTP: {self.otp}"

    def is_otp_expired(self):
        expiration_time = self.otp_created_at + timedelta(minutes=10)
        return timezone.now() > expiration_time
    