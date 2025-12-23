from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from student.models import Student
from Academics.models import AssignSubject,AssignClassTeacher
from Online_Exam.models import Exam
from instructor.models import Instructor

class StudentDashboardView(APIView):

    def post(self, request):
        
        try:
            student_id = request.data.get("student_id")

            if not student_id:
                return Response(
                    {"status": 0, "message": "student_id is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                student = Student.objects.select_related("section__cls").get(id=student_id)
            except Student.DoesNotExist:
                return Response(
                    {"status": 0, "message": "Student not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            if not student.section:
                return Response(
                    {"status": 0, "message": "Student section not assigned"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            classroom = student.section.cls
            section = student.section

            # ✅ CORRECT
            subjects_count = AssignSubject.objects.filter(
                classroom=classroom,
                section=section
            ).values("subject").distinct().count()

            exams_count = Exam.objects.filter(classroom=classroom).count()

            return Response({
                "status": 1,
                "data": {
                    "subjects_count": subjects_count,
                    "exams_count": exams_count
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":0,"error":str(e)},status=500) 

class InstructorDashboardView(APIView):
    def post(self,request):
        
        try:
            instructor_id=request.data.get("instructor_id")
                                       

            if not instructor_id:
                return Response({
                    "status":0,
                    "message":"instructor id is required"
                },status=status.HTTP_400_BAD_REQUEST)
        
            try:
                instructor=Instructor.objects.get(id=instructor_id)
            except Instructor.DoesNotExist:
                return Response({
                    "status":0,
                    "message":"instructor not found"
                },status=status.HTTP_404_NOT_FOUND) 

            subjects_count=AssignSubject.objects.filter(teacher=instructor).values("subject").distinct().count()

            classrooms_count=AssignClassTeacher.objects.filter(teacher=instructor).values("classroom").distinct().count()

            sections=AssignClassTeacher.objects.filter(teacher=instructor).values_list("section",flat=True).distinct()
            students_count=Student.objects.filter(section__in=sections).count()

            return Response({
                "status":1,
                "message":"instructor dashboard data fetched successfully",
                "data":{
                    "students_count":students_count,
                    "classrooms_count":classrooms_count,
                    "subjects_count":subjects_count
                }
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":0,"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)






