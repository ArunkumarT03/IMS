from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Online_Exam.models import Exam
from Academics.models import ClassRoom,Subject
from student.models import Student


class StudentDashboardView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        try:
            student=Student.object.get(user=request.user)
            student_class=student.ClassRoom
            if not student_class:
                return Response({
                    "status":0,
                    "message":"student class not assigned"
                },status=400)
            subject_count=Subject.objects.filter(ClassRoom=student_class).count()
            exams_count=Exam.objects.filter(ClassRoom=student_class).count()
            return Response({
                "status":1,
                "class":student_class.cls,
                "subjects_count":subject_count,
                "exams_count":exams_count

            },status=200)
        except Student.DoesNotExist:
            return Response({"status":0,"message":"student not found"},status=404)
        except Exception as e:
            return Response({"status":0,"error":str(e)},status=500)


 
