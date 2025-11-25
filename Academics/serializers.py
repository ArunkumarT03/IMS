from rest_framework import serializers
from Academics.models import *

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model= ClassRoom
        fields=['id','cls','sec']
        
        
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields=['id','subject_code','subject_name','type']
        