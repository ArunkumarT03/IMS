from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Instructor
from .serializers import InstructorSerializer

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

   