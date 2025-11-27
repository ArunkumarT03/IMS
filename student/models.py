from django.db import models
from users.models import *
from Academics.models import *

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile",null=True,blank=True)
    name = models.CharField(max_length=100)
    fathername = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=200, unique=True, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=100, choices=(('pending','Pending'),('approved','Approved')), default='pending')