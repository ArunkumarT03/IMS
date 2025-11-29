from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Instructor
from .serializers import InstructorSerializer
from django.contrib.auth import authenticate, login
from django.utils.timezone import localtime
from rest_framework_simplejwt.tokens import RefreshToken

class InstructorCreateView(APIView):
    def get(self, request):
        try:
            instructors = Instructor.objects.all()
            serializer = InstructorSerializer(instructors, many=True)
            return Response({
                "status": 1,
                "message": "Instructors retrieved successfully",
                "data": serializer.data
            }, status=200)
        except Exception as e:
            return Response({"status": 0, "error": str(e)}, status=500)

    def post(self, request):
        try:
            serializer = InstructorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": 1,
                    "message": "Instructor created successfully",
                    "data": serializer.data
                }, status=201)
            return Response({"status": 0, "errors": serializer.errors}, status=400)
        except Exception as e:
            return Response({"status": 0, "error": str(e)}, status=500)

    def put(self, request):
        try:
            instructor_id = request.data.get("id")

            if not instructor_id:
                return Response({
                    "status": 0,
                    "message": "Instructor ID is required for update"
                }, status=400)

            try:
                instructor = Instructor.objects.get(id=instructor_id)
            except Instructor.DoesNotExist:
                return Response({
                    "status": 0,
                    "message": "Instructor not found"
                }, status=404)

            serializer = InstructorSerializer(instructor, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": 1,
                    "message": "Instructor updated successfully",
                    "data": serializer.data
                }, status=200)

            return Response({"status": 0, "errors": serializer.errors}, status=400)

        except Exception as e:
            return Response({"status": 0, "error": str(e)}, status=500)
        
class GlobalLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"status": 0, "message": "Email and Password required"}, status=400)

        # Authenticate user
        user = authenticate(request, email=email, password=password)

        if not user:
            return Response({"status": 0, "message": "Invalid email or password"}, status=400)

        # Role-specific checks
        if user.role == "instructor":
            if not hasattr(user, "instructor_profile"):
                return Response({"status": 0, "message": "Instructor profile missing"}, status=400)
            
            # Optional: check if instructor is active
            if hasattr(user.instructor_profile, "is_active") and not user.instructor_profile.is_active:
                return Response({"status": 0, "message": "Instructor not active"}, status=403)

        elif user.role == "student":
            if not hasattr(user, "student_profile"):
                return Response({"status": 0, "message": "Student profile missing"}, status=400)
            if getattr(user.student_profile, "status", None) != "approved":
                return Response({"status": 0, "message": "Student not approved yet"}, status=403)

        # Log the user in (session login)
        login(request, user)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        # Serialize instructor info if role is instructor
        if user.role == "instructor":
            user_data = InstructorSerializer(user.instructor_profile).data
        else:
            user_data = {"id": user.id, "email": user.email, "role": user.role}

        last_login = localtime(user.last_login).strftime("%Y-%m-%d %H:%M:%S") if user.last_login else None

        return Response({
            "status": 1,
            "message": f"{user.role} login successful",
            "last_login": last_login,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": user_data
        }, status=200)