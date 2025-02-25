from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid
from datetime import timedelta

class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_field):
        if not email:
            raise ValueError('user must have an email address')
        
        user = self.model(email=email ,**extra_field)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, email, password):
        if not email:
            raise ValueError('user must have an email address')
        
        user = self.create_user(email, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=13)
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'{self.f_name} {self.l_name} : {self.email}'

class PasswordResetToken(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Token is valid for 10 minutes
        return timezone.now() < self.created_at + timedelta(minutes=10)
    
    def __str__(self):
        return f'Token for {self.user.email} created at {self.created_at}'
