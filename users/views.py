from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import *

class UserDeleteView(APIView):
    def delete(self,request,pk):
        user=User.objects.get(id=pk)
        if not user:
            return Response({'message':'user not found'},status=400)
        user.delete()
        return Response({'message':'user deleted'})
    
        
        