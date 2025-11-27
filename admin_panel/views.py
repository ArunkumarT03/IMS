from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from admin_panel.serializers import *
from student.models import *
# Create your views here.
class AdminSignupView(APIView):
    def post(self, request):
        serializer = AdminSignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": 1, "message": "Admin created successfully"}, status=201)

        return Response({"status": 0, "errors": serializer.errors}, status=400)
    
class ApproveStudentView(APIView):

    def post(self, request, pk):

        if not request.user.is_authenticated:
            return Response({"status": 0, "message": "Authentication required"}, status=401)

        if request.user.role != "admin":   
            return Response({"status": 0, "message": "Only admin can approve students"}, status=403)

        # Fetch student
        try:
            student = Student.objects.get(id=pk)
        except Student.DoesNotExist:
            return Response({"status": 0, "message": "Student not found"}, status=404)

        # Update approval
        student.status = "approved"
        student.save()

        return Response({"status": 1, "message": "Student approved successfully"}, status=200)