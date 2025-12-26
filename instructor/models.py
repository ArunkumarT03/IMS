from django.db import models
from users.models import User
from Academics.models import Subject

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="instructor_profile",null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True,null=True,blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    qualification = models.CharField(max_length=150)
    experience = models.CharField(max_length=50)
    subjects = models.ManyToManyField(Subject, related_name="instructors")
    is_active = models.BooleanField(default=True)  # Optional
    
    def __str__(self):
        return self.name
