from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from datetime import timedelta
from hoteldetails.models import HotelDetails
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings

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
        return self.create_user(email, user_name,password, **extra_fields)

class User(AbstractUser):

    ROLE_CHOICES = (
        ('Admin','Admin'),
        ('Manager','Manager'),
        ('Receptionist', 'Receptionist'),
        ('Staff', 'Staff')
    )

    username = None 
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=150, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES,default='Admin')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"
    

class EmailOTP(models.Model):
    
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True )
    otp = models.IntegerField(null=True, blank=True)
    otp_created_at = models.DateTimeField(auto_now=True)
    user_name = models.CharField(max_length=150)  
    password = models.CharField(max_length=128)   
    forgot=models.BooleanField(default= False, blank= True)
    otp_verified = models.BooleanField(default=False, blank=True)
    
    def __str__(self):
        return f"{self.email} - OTP: {self.otp}"

    def is_otp_expired(self):
        expiration_time = self.otp_created_at + timedelta(minutes=10)
        return timezone.now() > expiration_time
    
class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_hotels')
    hotel = models.ForeignKey('hoteldetails.HotelDetails', on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, default='Manager')
    password = models.CharField(max_length=50)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # New instance
            # Create user account
            user = User.objects.create_user(
                email=self.email,
                user_name=self.name,
                password=get_random_string(10),
                role='Manager'
            )
            self.user = user
            self.send_registration_email()
        super().save(*args, **kwargs)

        
    def send_registration_email(self):
        subject = "Registration Successful"
        message = (
            f"Dear {self.name},\n\n"
            f"Your account as a Manager has been successfully created.\n"
            f"Your login credentials are:\n"
            f"Email: {self.email}\n"
            f"Password: {self.password}\n\n"
            "Regards,\nThe Team"
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])

    def __str__(self):
        return f"{self.name} ({self.role})"

class Receptionist(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receptionists')
    hotel = models.ForeignKey(HotelDetails, on_delete=models.CASCADE, related_name='receptionists')
    manager = models.ForeignKey(Manager,on_delete= models.CASCADE , related_name='receptionists')
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, default='Receptionist')
    password = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.pk:  # if this is a new instance
            if not self.password:
                self.password = get_random_string(10)
                
            user = User.objects.create_user(
                email=self.email,
                user_name=self.name,
                password=self.password,  # Ensure a password is set here
                role='Receptionist'  # Assign the role
            )
            self.admin=user
            # self.hotel=hotel
            self.send_registration_email()
        
        super().save(*args, **kwargs)

    def send_registration_email(self):
        subject = "Receptionist Registration Successful"
        message = (
            f"Dear {self.name},\n\n"
            f"Your account as a Receptionist has been successfully created.\n"
            f"Your login credentials are:\n"
            f"Email: {self.email}\n"
            f"Password: {self.password}\n\n"
            "Regards,\nThe Team"
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])

    def __str__(self):
        return f"{self.name} ({self.role})"    

class Staff(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff')
    hotel = models.ForeignKey(HotelDetails, on_delete=models.CASCADE, related_name='staff')
    manager = models.ForeignKey(Manager ,on_delete= models.CASCADE , related_name='staff')
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, default='Staff')
    sub_role = models.CharField(max_length=50, default='housekeeping')
    password = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.pk:  # if this is a new instance
            if not self.password:
                self.password = get_random_string(10)
            user = User.objects.create_user(
                email=self.email,
                user_name=self.name,
                password=self.password,  # Ensure a password is set here
                role='Staff'  # Assign the role
            )
            self.admin = user  # Associate with the admin
            # self.hotel = hotel
            self.send_registration_email()
        
        super().save(*args, **kwargs)

    def send_registration_email(self):
        subject = "Staff Registration Successful"
        message = (
            f"Dear {self.name},\n\n"
            f"Your account has been successfully created in the {self.role} department.\n"
            f"Your login credentials are:\n"
            f"Email: {self.email}\n"
            f"Password: {self.password}\n\n"
            "Regards,\nThe Team"
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])

    def __str__(self):
        return f"{self.name} ({self.role})"
    
class Token(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='auth_token', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key