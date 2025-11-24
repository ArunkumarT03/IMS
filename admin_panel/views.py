from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from admin_panel.serializers import *
# Create your views here.
class AdminSignupView(APIView):
    def post(self, request):
        serializer = AdminSignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": 1, "message": "Admin created successfully"}, status=201)

        return Response({"status": 0, "errors": serializer.errors}, status=400)