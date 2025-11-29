from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from Academics.models import *
from Academics.serializers import *
from rest_framework import status

class CreateClassroomView(APIView):
    def get(self, request):
        classrooms = ClassRoom.objects.all()
        serializer = ClassroomSerializer(classrooms, many=True)
        
        return Response({
            "status": 1,
            "message": "Classrooms fetched successfully",
            "data": serializer.data
        }, status=200)
    
    def post(self, request):
        serializer = CreateClassroomSerializer(data=request.data)
        if serializer.is_valid():
            classroom = serializer.save()
            return Response({
                "status": 1,
                "message": "Classroom created successfully",
                "data": ClassroomSerializer(classroom).data
            })
        return Response({"status": 0, "errors": serializer.errors}, status=400)
        
class SubjectView(APIView):
    def get(self,request):
        sub_data=Subject.objects.all()
        sub_serializer=SubjectSerializer(sub_data,many=True)
        return Response({
            "status": 1,
            "message": "subjects fetched successfully",
            "data":sub_serializer.data
        },status=200)
    def post(self,request):
        sub_data=SubjectSerializer(data=request.data)
        try:
            if sub_data.is_valid():
                sub_data.save()
                return Response({'status':1,'message':'subject created'})
            return Response({'status':0,'error':sub_data.errors},status=400)
        except Exception as e:
            return Response({'error':str(e)},status=500)
        



# AssignSubject POST view
class AssignSubjectView(APIView):
     def get(self, request):
        assign_subjects = AssignSubject.objects.all()
        data = []
        for a in assign_subjects:
            data.append({
                "id": a.id,
                "classroom": a.classroom.cls,
                "section": a.section.sec,
                "subject": a.subject.subject_name,
                "teacher": a.teacher.name
            })
        return Response({
            "status": 1,
            "message": "Assigned subjects fetched successfully",
            "data": data
        }, status=status.HTTP_200_OK)
     def post(self, request):
        serializer = CreateAssignSubjectSerializer(data=request.data)
        try:
        
         if serializer.is_valid():
                assign_subject = serializer.save()
                return Response({
                    "id": assign_subject.id,
                    "classroom": assign_subject.classroom.cls,
                    "section": assign_subject.section.sec,
                    "subject": assign_subject.subject.subject_name,
                    "teacher": assign_subject.teacher.name
                }, status=status.HTTP_201_CREATED)
         else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)})

# AssignClassTeacher POST view
class AssignClassTeacherView(APIView):
    def get(self, request):
        assign_teachers = AssignClassTeacher.objects.all()
        data = []
        for a in assign_teachers:
            data.append({
                "id": a.id,
                "classroom": a.classroom.cls,
                "section": a.section.sec,
                "teacher": a.teacher.name,
                
            })
        return Response({
            "status": 1,
            "message": "Assigned class teachers fetched successfully",
            "data": data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateAssignClassTeacherSerializer(data=request.data)
        try:

            if serializer.is_valid():
                    assign_teacher = serializer.save()
                    return Response({
                        "id": assign_teacher.id,
                        "classroom": assign_teacher.classroom.cls,
                        "section": assign_teacher.section.sec,
                        "teacher": assign_teacher.teacher.name,
                        "role": assign_teacher.role
                    }, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)})