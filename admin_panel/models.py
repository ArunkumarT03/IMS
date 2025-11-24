from django.db import models
from users.models import *
# Create your models here.
class Admin_panel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admin_profile",null=True,blank=True)
    email = models.EmailField(max_length=200, unique=True, null=True, blank=True)
    