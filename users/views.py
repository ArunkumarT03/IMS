from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import *

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
        return Response(
            {"status": 1, "message": "User deleted successfully"},
            status=200
        )

    

         
  