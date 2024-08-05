from django.db import models
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from .enums import UserType

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, user_type, **extra_fields):
        # **extra_fields are the fields that come with the default django user model
        if not email:
            raise ValueError("Email must be provided!!")
        if not password:
            raise ValueError("Password must be provided!!")
        
        # to create the user object
        user = self.model(
            email=self.normalize_email(email),
            user_type=user_type,
            **extra_fields
        )

        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, user_type, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser is_staff must be 'True'")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser is_superuser must b e 'True'")

        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser is_active must be 'True'")

        return self.create_user(email=email, password=password,
                                user_type=user_type, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    

    # std_user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    username = models.CharField(max_length=250, null=False, unique=True)
    email = models.EmailField(max_length=250, null=False, unique=True)
    phone_number = models.CharField(max_length=14, null=True)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField()
    user_type = models.CharField(max_length=10, choices=UserType, default=UserType.STUDENT)
    date_created = models.DateTimeField(auto_now_add=True)

    # create UserManager object to use this custom model.
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    # A list of the field names that will be prompted for when creating a superuser.
    REQUIRED_FIELDS = ['username', 'date_of_birth', 'user_type']

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"Username: {self.username}>> email: {self.email}"

    

