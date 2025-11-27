from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from Academics.models import *
from Academics.serializers import *

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
        
