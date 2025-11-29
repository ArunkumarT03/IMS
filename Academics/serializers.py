from rest_framework import serializers
from Academics.models import *
from instructor.models import *

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
    # Ensure 'type' only accepts valid choices
    type = serializers.ChoiceField(choices=Subject.SUBJECT_TYPES)

    class Meta:
        model = Subject
        fields = ['id', 'subject_code', 'subject_name', 'type']    

# Serializer for AssignSubject input (POST)
class CreateAssignSubjectSerializer(serializers.Serializer):
    classroom = serializers.CharField()
    section = serializers.CharField()
    subject = serializers.CharField()
    teacher = serializers.CharField()

    def create(self, validated_data):
        classroom_name = validated_data['classroom']
        section_name= validated_data['section']
        subject_name = validated_data['subject']
        teacher_name = validated_data['teacher']

        classroom = ClassRoom.objects.get(cls=classroom_name)
        section = Section.objects.get(sec=section_name)
        subject = Subject.objects.get(subject_name=subject_name)
        teacher = Instructor.objects.get(name=teacher_name)

        assign_subject, created = AssignSubject.objects.get_or_create(
            classroom=classroom,
            section=section,
            subject=subject,
            defaults={'teacher': teacher}  # use defaults for get_or_create
        )

        # If the object exists, update teacher
        if not created:
            assign_subject.teacher = teacher
            assign_subject.save()

        return assign_subject


# Serializer for AssignClassTeacher input (POST)
class CreateAssignClassTeacherSerializer(serializers.Serializer):
    classroom = serializers.CharField()
    section = serializers.CharField()
    teacher = serializers.CharField()
    role = serializers.ChoiceField(choices=[('class_teacher', 'Class Teacher'),
                                            ('assistant_teacher', 'Assistant Teacher'),
                                            ('hod', 'HOD')])

    def create(self, validated_data):
        classroom_name = validated_data['classroom']
        section_name = validated_data['section']
        teacher_name = validated_data['teacher']
        role = validated_data['role']

        classroom = ClassRoom.objects.get(cls=classroom_name)
        section = Section.objects.get(sec=section_name)
        teacher = Instructor.objects.get(name=teacher_name)

        assign_teacher, created = AssignClassTeacher.objects.get_or_create(
            classroom=classroom,
            section=section,
            teacher=teacher,
            defaults={'role': role}
        )

        # If exists, update role
        if not created:
            assign_teacher.role = role
            assign_teacher.save()

        return assign_teacher