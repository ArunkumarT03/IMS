from django.shortcuts import render,get_object_or_404

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import *
from rest_framework import status

class UserDeleteView(APIView):
    def delete(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(
                {"status": 0, "message": "User not found"},
                status=404
            )

        user.delete()
        return Response({'message':'user deleted'})
    
        
        