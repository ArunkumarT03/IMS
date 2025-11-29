from rest_framework import serializers
from .models import Instructor
from Academics.models import Subject 


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'subject_name', 'subject_code']


class InstructorSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    subject_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Subject.objects.all(), 
        write_only=True,
        source='subjects' 
    )

    class Meta:
        model = Instructor
        fields = [
            'id', 
            'name', 
            'email', 
            'phone', 
            'qualification', 
            'experience', 
            'subjects',   # For reading/displaying data
            'subject_ids' # For writing/receiving data
        ]
        read_only_fields = ['id']