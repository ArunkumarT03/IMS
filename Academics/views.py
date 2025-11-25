from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from Academics.models import *
from Academics.serializers import *

class ClassroomView(APIView):
    def post(self,request):
        cls_data=ClassroomSerializer(data=request.data)
        try:
            if cls_data.is_valid():
                cls_data.save()
                return Response({'status':1,'message':'class and section created'},status=201)
            return Response({'status':0,'error':cls_data.errors},status=400)
        except Exception as e:
            return Response({'error':str(e)},status=500)
        
class SubjectView(APIView):
    def post(self,request):
        sub_data=SubjectSerializer(data=request.data)
        try:
            if sub_data.is_valid():
                sub_data.save()
                return Response({'status':1,'message':'subject created'})
            return Response({'status':0,'error':sub_data.errors},status=400)
        except Exception as e:
            return Response({'error':str(e)},status=500)
        
