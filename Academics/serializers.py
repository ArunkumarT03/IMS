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


class SubjectTeacherPairSerializer(serializers.Serializer):
    subject = serializers.CharField()
    teacher = serializers.CharField()


class CreateAssignSubjectSerializer(serializers.Serializer):
    classroom = serializers.CharField()
    section = serializers.CharField()
    assignments = SubjectTeacherPairSerializer(many=True)

    def create(self, validated_data):
        classroom_name = validated_data['classroom']
        section_name = validated_data['section']
        assignment_list = validated_data['assignments']

        # Validate classroom
        try:
            classroom = ClassRoom.objects.get(cls=classroom_name)
        except ClassRoom.DoesNotExist:
            raise serializers.ValidationError({"classroom": f"ClassRoom '{classroom_name}' does not exist"})

        # Validate section
        try:
            section = Section.objects.get(sec=section_name)
        except Section.DoesNotExist:
            raise serializers.ValidationError({"section": f"Section '{section_name}' does not exist"})

        created_items = []

        for item in assignment_list:
            subject_name = item["subject"]
            teacher_name = item["teacher"]

            # validate subject
            try:
                subject = Subject.objects.get(subject_name=subject_name)
            except Subject.DoesNotExist:
                raise serializers.ValidationError({"subject": f"Subject '{subject_name}' does not exist"})

            # validate teacher
            try:
                teacher = Instructor.objects.get(name=teacher_name)
            except Instructor.DoesNotExist:
                raise serializers.ValidationError({"teacher": f"Teacher '{teacher_name}' does not exist"})

            # create or update assignment
            assign_sub, created = AssignSubject.objects.get_or_create(
                classroom=classroom,
                section=section,
                subject=subject,
                defaults={'teacher': teacher}
            )

            if not created:
                assign_sub.teacher = teacher
                assign_sub.save()

            created_items.append(assign_sub)

        return created_items

class TeacherAssignmentSerializer(serializers.Serializer):
    teacher = serializers.CharField()
    role = serializers.ChoiceField(choices=[
        ('class_teacher', 'Class Teacher'),
        ('assistant_teacher', 'Assistant Teacher'),
        ('hod', 'HOD')
    ])

class AssignMultipleTeachersSerializer(serializers.Serializer):
    classroom = serializers.CharField()
    section = serializers.CharField()
    assignments = TeacherAssignmentSerializer(many=True)

    def create(self, validated_data):
        classroom_name = validated_data["classroom"]
        section_name = validated_data["section"]
        assignments = validated_data["assignments"]

        # Classroom
        try:
            classroom = ClassRoom.objects.get(cls=classroom_name)
        except ClassRoom.DoesNotExist:
            raise serializers.ValidationError({"classroom": f"ClassRoom '{classroom_name}' does not exist"})

        # Section
        try:
            section = Section.objects.get(sec=section_name)
        except Section.DoesNotExist:
            raise serializers.ValidationError({"section": f"Section '{section_name}' does not exist"})

        saved_assignments = []

        for item in assignments:
            teacher_name = item["teacher"]
            role = item["role"]

            # Teacher
            try:
                teacher = Instructor.objects.get(name__iexact=teacher_name)
            except Instructor.DoesNotExist:
                raise serializers.ValidationError({"teacher": f"Instructor '{teacher_name}' does not exist"})

            # Create or update
            obj, created = AssignClassTeacher.objects.get_or_create(
                classroom=classroom,
                section=section,
                teacher=teacher,
                defaults={"role": role}
            )

            if not created:
                obj.role = role
                obj.save()

            saved_assignments.append({
                "teacher": teacher_name,
                "role": role,
                "status": "created" if created else "updated"
            })

        return {"assignments": saved_assignments}
