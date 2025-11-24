from django.db import models
from users.models import *

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile",null=True,blank=True)
    name = models.CharField(max_length=100)
    fathername = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=200, unique=True, null=True, blank=True)
    cls = models.CharField(max_length=100)
    sec = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=(('pending','Pending'),('approved','Approved')), default='pending')