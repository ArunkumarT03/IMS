from django.db import models
from Academics.models import Subject 

class Instructor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True) 
    qualification = models.CharField(max_length=150)
    experience = models.CharField(max_length=50) 
    subjects = models.ManyToManyField(Subject, related_name='instructors')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Instructor"
        verbose_name_plural = "Instructors"
