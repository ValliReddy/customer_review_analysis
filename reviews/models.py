from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import bcrypt

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, name=None):
        if not email:
            raise ValueError("The Email field must be set")
        user = self.model(email=email, name=name)
        user.set_password(password)  # This will hash the password properly
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, name=None):
        user = self.create_user(email, password, name)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Add this line
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def check_password(self, password):
        # You do not need to manually check the password if you use set_password and check_password methods of Django.
        return super().check_password(password)
