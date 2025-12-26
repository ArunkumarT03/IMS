from django.shortcuts import render,get_object_or_404

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from student.models import Student
from admin_panel.models import Admin_panel
from instructor.models import Instructor

class UserDeleteView(APIView):
    

    def delete(self, request, role, pk):
        try:
            # Get profile
            if role == "student":
                profile = Student.objects.filter(pk=pk).first()
            elif role == "admin":
                profile = Admin_panel.objects.filter(pk=pk).first()
            elif role == "instructor":
                profile = Instructor.objects.filter(pk=pk).first()
            else:
                return Response(
                    {"status": 0, "message": "Invalid role"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not profile:
                return Response(
                    {"status": 0, "message": f"{role.capitalize()} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Delete linked user if it exists
            user = getattr(profile, "user", None)
            if user:
                if not user.is_active:
                    user.delete()  # CASCADE deletes profile
                else:
                    # Active user → delete profile only
                    profile.delete()
            else:
                # No linked user → delete profile only
                profile.delete()

            return Response(
                {"status": 1, "message": f"{role.capitalize()} deleted successfully"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"status": 0, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
