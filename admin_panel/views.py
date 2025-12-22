from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from admin_panel.serializers import *
from student.models import *
from rest_framework import status
from instructor.models import *
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
    
    
class AdminDashboard(APIView):

    def post(self, request):
        admin_id = request.data.get("admin_id")

        if not admin_id:
            return Response(
                {"status": 0, "message": "admin_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            admin_user = User.objects.get(id=admin_id)
        except User.DoesNotExist:
            return Response(
                {"status": 0, "message": "Admin not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if admin_user.role != "admin":
            return Response(
                {"status": 0, "message": "Access denied. Admin only"},
                status=status.HTTP_403_FORBIDDEN
            )

       
        students_count = Student.objects.count()
        approved_students = Student.objects.filter(status="approved").count()
        pending_students = Student.objects.filter(status="pending").count()

        instructors_count = Instructor.objects.count()
        subjects_count = Subject.objects.count()
        classrooms_count = ClassRoom.objects.count()
        sections_count = Section.objects.count()

        return Response({
            "status": 1,
            "message": "Admin dashboard data fetched successfully",
            "data": {
                "students": {
                    "total": students_count,
                    "approved": approved_students,
                    "pending": pending_students
                },
                "instructors": instructors_count,
                "subjects": subjects_count,
                "classrooms": classrooms_count,
                "sections": sections_count
            }
        }, status=status.HTTP_200_OK)
        
        