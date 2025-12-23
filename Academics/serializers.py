from rest_framework import serializers
from Academics.models import *
from instructor.models import *

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id','sec']

# Classroom serializer with nested sections
class ClassroomSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = ClassRoom
        fields = ['id','cls','sections']

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
    def update(self, instance, validated_data):
        instance.cls = validated_data.get("cls", instance.cls)
        instance.save()
        new_sections = validated_data.get("sec", [])
        Section.objects.filter(cls=instance).delete()
        for s in new_sections:
            Section.objects.get_or_create(cls=instance, sec=s)

        return instance

class SubjectSerializer(serializers.ModelSerializer):
    # Ensure 'type' only accepts valid choices
    type = serializers.ChoiceField(choices=Subject.SUBJECT_TYPES)

    class Meta:
        model = Subject
        fields = ['id', 'subject_code', 'subject_name', 'type']    


class SubjectTeacherPairSerializer(serializers.Serializer):
    subject = serializers.CharField()
    teacher = serializers.ListField(child=serializers.CharField(), required=True)

class AssignSubjectListSerializer(serializers.ModelSerializer):
    classroom = serializers.CharField(source="classroom.cls", read_only=True)
    section = serializers.CharField(source="section.sec", read_only=True)
    subject = serializers.CharField(source="subject.subject_name", read_only=True)
    teacher = serializers.SerializerMethodField()  

    class Meta:
        model = AssignSubject
        fields = ['id', 'classroom', 'section', 'subject', 'teacher']

    def get_teacher(self, obj):
        # return list of teacher names
         return [t.name for t in obj.teacher.all()]



class CreateAssignSubjectSerializer(serializers.Serializer):
    classroom = serializers.CharField()
    section = serializers.CharField()
    assignments = SubjectTeacherPairSerializer(many=True)

    def _get_classroom_section(self, classroom, section):
        try:
            cls = ClassRoom.objects.get(cls__iexact=classroom)
            sec = Section.objects.get(cls=cls, sec__iexact=section)
            return cls, sec
        except ClassRoom.DoesNotExist:
            raise serializers.ValidationError({"classroom": "Invalid classroom"})
        except Section.DoesNotExist:
            raise serializers.ValidationError({"section": "Invalid section"})

    def _get_subject_teachers(self, item):
        try:
            subject = Subject.objects.get(subject_name__iexact=item["subject"].strip())
        except Subject.DoesNotExist:
            raise serializers.ValidationError({"subject": "Invalid subject"})

        teachers = Instructor.objects.filter(name__in=item["teacher"])
        if teachers.count() != len(item["teacher"]):
            raise serializers.ValidationError({"teacher": "Invalid teacher name"})

        return subject, teachers

    def create(self, validated_data):
        classroom, section = self._get_classroom_section(
            validated_data["classroom"], validated_data["section"]
        )

        results = []
        for item in validated_data["assignments"]:
            subject, teachers = self._get_subject_teachers(item)

            obj, _ = AssignSubject.objects.update_or_create(
                classroom=classroom,
                section=section,
                subject=subject
            )
            obj.teacher.set(teachers)

            results.append({
                "subject": subject.subject_name,
                "teacher": [t.name for t in teachers]
            })

        return {
            "classroom": classroom.cls,
            "section": section.sec,
            "assignments": results
        }

    def update(self, instance, validated_data):
        classroom, section = self._get_classroom_section(
            validated_data["classroom"], validated_data["section"]
        )

        item = validated_data["assignments"][0]
        subject, teachers = self._get_subject_teachers(item)

        instance.classroom = classroom
        instance.section = section
        instance.subject = subject
        instance.save()
        instance.teacher.set(teachers)

        return {
            "classroom": classroom.cls,
            "section": section.sec,
            "assignments": [{
                "subject": subject.subject_name,
                "teacher": [t.name for t in teachers],
                "status": "updated"
            }]
        }


class TeacherAssignmentSerializer(serializers.Serializer):
    teacher = serializers.CharField()
    role = serializers.ChoiceField(choices=[
        ('class_teacher', 'Class Teacher'),
        ('assistant_teacher', 'Assistant Teacher'),
        ('hod', 'HOD')
    ])

class AssignClassTeacherListSerializer(serializers.ModelSerializer):
    classroom = serializers.CharField(source='classroom.cls', read_only=True)
    section = serializers.CharField(source='section.sec', read_only=True)
    teacher = serializers.CharField(source='teacher.name',read_only=True)

    class Meta:
        model = AssignClassTeacher
        fields = ['id', 'classroom', 'section', 'teacher','role']


class AssignMultipleTeachersSerializer(serializers.Serializer):
    classroom = serializers.CharField()
    section = serializers.CharField()
    assignments = TeacherAssignmentSerializer(many=True)

    def validate(self, data):
        roles = [a["role"] for a in data["assignments"]]
        if len(roles) != len(set(roles)):
            raise serializers.ValidationError(
                "Each role must be unique for this class & section."
            )
        return data

    def create(self, validated_data):
        # 🔹 Convert classroom name → ClassRoom object
        try:
            classroom_obj = ClassRoom.objects.get(
                cls__iexact=validated_data["classroom"]
            )
        except ClassRoom.DoesNotExist:
            raise serializers.ValidationError({
                "classroom": "Classroom does not exist"
            })

        # 🔹 Convert section name → Section object
        try:
            section_obj = Section.objects.get(
                cls=classroom_obj,
                sec__iexact=validated_data["section"]
            )
        except Section.DoesNotExist:
            raise serializers.ValidationError({
                "section": "Section does not exist for this classroom"
            })

        saved_assignments = []

        for item in validated_data["assignments"]:
            teacher_name = item["teacher"]
            role = item["role"]

            # 🔹 SAFE teacher lookup (no get())
            teacher_qs = Instructor.objects.filter(
                name__iexact=teacher_name
            )

            if not teacher_qs.exists():
                raise serializers.ValidationError({
                    "teacher": f"Instructor '{teacher_name}' does not exist"
                })

            if teacher_qs.count() > 1:
                raise serializers.ValidationError({
                    "teacher": (
                        f"Multiple instructors found with name '{teacher_name}'. "
                        "Use unique identifier."
                    )
                })

            teacher_obj = teacher_qs.first()

            # 🔹 Save using MODEL OBJECTS
            obj, created = AssignClassTeacher.objects.update_or_create(
                classroom=classroom_obj,
                section=section_obj,
                teacher=teacher_obj,
                defaults={"role": role}
            )

            saved_assignments.append({
                "teacher": teacher_obj.name,
                "role": role,
                "status": "created" if created else "updated"
            })

        return {
            "classroom": classroom_obj.cls,
            "section": section_obj.sec,
            "assignments": saved_assignments
        }
    def update(self, instance, validated_data):
        classroom_obj = ClassRoom.objects.get(
            cls__iexact=validated_data["classroom"]
        )
        section_obj = Section.objects.get(
            cls=classroom_obj,
            sec__iexact=validated_data["section"]
        )

        item = validated_data["assignments"][0]

        teacher_obj = Instructor.objects.get(
            name__iexact=item["teacher"]
        )

        instance.classroom = classroom_obj
        instance.section = section_obj
        instance.teacher = teacher_obj
        instance.role = item["role"]
        instance.save()

        return {
            "classroom": classroom_obj.cls,
            "section": section_obj.sec,
            "assignments": [
                {
                    "teacher": teacher_obj.name,
                    "role": instance.role,
                    "status": "updated"
                }
            ]
        }


class RoleOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignClassTeacher
        fields = ['role']
    
  