from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, role="student", **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)   # uses Django’s hashing
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        return self.create_user(email=email, password=password, role="admin", **extra_fields)


class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("student", "Student"),
        ("instructor", "Instructor"),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # nothing else required

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"