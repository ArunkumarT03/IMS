from django.shortcuts import render,get_object_or_404

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import *
from rest_framework import status
from student.models import *
from admin_panel.models import *
from instructor.models import *

class UserDeleteView(APIView):
    def delete(self, request, role, pk):

        try:
            if role == "student":
                profile = Student.objects.get(pk=pk)
                user = profile.user

            elif role == "admin":
                profile = Admin_panel.objects.get(pk=pk)
                user = profile.user

            elif role == "instructor":
                profile = Instructor.objects.get(pk=pk)
                user = profile.user

            else:
                return Response(
                    {"status": 0, "message": "Invalid role"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not user:
                return Response(
                    {"status": 0, "message": "Linked user not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            user.delete()   # ✅ CASCADE deletes profile

            return Response(
                {"status": 1, "message": f"{role.capitalize()} deleted successfully"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"status": 0, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        