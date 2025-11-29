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
      if serializer.is_valid():
        assigned = serializer.save()

        response = []
        for a in assigned:
            response.append({
                "id": a.id,
                "classroom": a.classroom.cls,
                "section": a.section.sec,
                "subject": a.subject.subject_name,
                "teacher": a.teacher.name
            })

        return Response({
            "status": 1,
            "message": "Assignments saved successfully!",
            "data": response
        }, status=status.HTTP_201_CREATED)

      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 

        
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
        serializer = AssignMultipleTeachersSerializer(data=request.data)

        if serializer.is_valid():
            result = serializer.save()
            return Response({
                "status": 1,
                "message": "Teachers assigned successfully",
                "data": result
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": 0,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)