from rest_framework import serializers
from Academics.models import *

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['sec']

# Classroom serializer with nested sections
class ClassroomSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = ClassRoom
        fields = ['cls', 'sections']

# Serializer for input (POST request)
class CreateClassroomSerializer(serializers.Serializer):
    cls = serializers.CharField()
    sec = serializers.ListField(child=serializers.CharField())

    def create(self, validated_data):
        cls_name = validated_data['cls']
        sec_list = validated_data['sec']

        classroom, created = ClassRoom.objects.get_or_create(cls=cls_name)

        for s in sec_list:
            Section.objects.get_or_create(cls=classroom, sec=s)

        return classroom

        
        
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields=['id','subject_code','subject_name','type']
        