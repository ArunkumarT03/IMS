from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from student.serializers import *
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import localtime
# Create your views here.
class StudentSignupView(APIView):
    def post(self, request):
        serializer = StudentSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"status": 1, "message": "Student created successfully"}, status=201)

        return Response({"status": 0, "errors": serializer.errors}, status=400)
    
    
class GlobalLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"status": 0, "message": "Email and Password required"}, status=400)

        user = authenticate(request, email=email, password=password)

        if not user:
            return Response({"status": 0, "message": "Invalid email or password"}, status=400)

        # ⬅️ THIS IS THE IMPORTANT PART
        login(request, user)  # This updates last_login in DB

        # generate tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            "status": 1,
            "message": f"{user.role} login successful",
            "role": user.role,
            "email": user.email,
            "last_login": localtime(user.last_login).strftime("%Y-%m-%d %H:%M:%S"),  # return updated last_login
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }, status=200)