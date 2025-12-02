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
    teacher = serializers.ListField(child=serializers.CharField(), required=True)

class AssignSubjectListSerializer(serializers.ModelSerializer):
    classroom = serializers.PrimaryKeyRelatedField(read_only=True)
    section = serializers.PrimaryKeyRelatedField(read_only=True)
    subject = serializers.CharField(source="subject.subject_name", read_only=True)
    teacher = serializers.SerializerMethodField()  

    class Meta:
        model = AssignSubject
        fields = ['id', 'classroom', 'section', 'subject', 'teacher']

    def get_teacher(self, obj):
        # return list of teacher names
         return [t.name for t in obj.teacher.all()]



class CreateAssignSubjectSerializer(serializers.Serializer):
    classroom = serializers.PrimaryKeyRelatedField(queryset=ClassRoom.objects.all(), required=False)
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all(), required=False)
    assignments = SubjectTeacherPairSerializer(many=True)
    class Meta:
        model = AssignSubject
        fields = ['id', 'classroom', 'section', 'subject', 'teacher']

    def create(self, validated_data):
        classroom = validated_data['classroom']
        section = validated_data['section']
        assignment_list = validated_data['assignments']

        created_items = []

        for item in assignment_list:
            subject_name = item["subject"].strip()
            teacher_names = item["teacher"]  # list of teacher names

            # Validate subject
            try:
                subject = Subject.objects.get(subject_name=subject_name)
            except Subject.DoesNotExist:
                raise serializers.ValidationError(
                    {"subject": f"Subject '{subject_name}' does not exist"}
                )

            # Validate teachers
            teachers_qs = Instructor.objects.filter(name__in=teacher_names)
            if teachers_qs.count() != len(teacher_names):
                existing = set(t.name for t in teachers_qs)
                missing = set(teacher_names) - existing
                raise serializers.ValidationError(
                    {"teacher": f"Teachers '{', '.join(missing)}' do not exist"}
                )

            # Create or update assignment
            assign_sub, created = AssignSubject.objects.get_or_create(
                classroom=classroom,
                section=section,
                subject=subject,
            )

            assign_sub.teacher.set(teachers_qs)
            assign_sub.save()

            created_items.append(assign_sub)

        return created_items
   
    def update(self, instance, validated_data):
  

    # Extract new classroom/section
        instance.classroom = validated_data.get("classroom", instance.classroom)
        instance.section = validated_data.get("section", instance.section)

    # Only one assignment allowed in update
        assignment = validated_data["assignments"][0]
        subject_name = assignment["subject"].strip()
        teacher_names = assignment["teacher"]

    # Validate subject
        try:
            subject = Subject.objects.get(subject_name=subject_name)
        except Subject.DoesNotExist:
            raise serializers.ValidationError(
                {"subject": f"Subject '{subject_name}' does not exist"}
        )

    # Check if another AssignSubject exists with same classroom/section/subject
        existing = AssignSubject.objects.filter(
            classroom=instance.classroom,
            section=instance.section,
            subject=subject
        ).exclude(pk=instance.pk).first()

        if existing:
            raise serializers.ValidationError({
                "error": "Another assignment already exists with this classroom, section, and subject."
        })

    # Validate teachers
        teachers = Instructor.objects.filter(name__in=teacher_names)
        if teachers.count() != len(teacher_names):
            missing = set(teacher_names) - set(t.name for t in teachers)
            raise serializers.ValidationError(
                {"teacher": f"Teachers not found: {', '.join(missing)}"}
        )

    # Update instance
        instance.classroom = instance.classroom
        instance.section = instance.section
        instance.subject = subject
        instance.save()

    # Update teachers
        instance.teacher.set(teachers)

        return instance

    def save(self, **kwargs):
        if self.instance:
            return self.update(self.instance, self.validated_data)
        return self.create(self.validated_data)



class TeacherAssignmentSerializer(serializers.Serializer):
    teacher = serializers.CharField()
    role = serializers.ChoiceField(choices=[
        ('class_teacher', 'Class Teacher'),
        ('assistant_teacher', 'Assistant Teacher'),
        ('hod', 'HOD')
    ])

class AssignClassTeacherListSerializer(serializers.ModelSerializer):
    classroom = serializers.PrimaryKeyRelatedField(read_only=True)
    section = serializers.PrimaryKeyRelatedField(read_only=True)
    teacher = serializers.CharField(source='teacher.name', read_only=True)

    class Meta:
        model = AssignClassTeacher
        fields = ['id', 'classroom', 'section', 'teacher', 'role']


class AssignMultipleTeachersSerializer(serializers.Serializer):
    classroom = serializers.PrimaryKeyRelatedField(queryset=ClassRoom.objects.all())
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())
    assignments = TeacherAssignmentSerializer(many=True)

    def create(self, validated_data):
        classroom = validated_data["classroom"]
        section = validated_data["section"]
        assignments = validated_data["assignments"]

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

        return {
            "classroom": classroom.id,
            "section": section.id,
            "assignments": saved_assignments
        }
   
    def update(self, instance, validated_data):
        classroom = validated_data.get('classroom', instance.classroom)
        section = validated_data.get('section', instance.section)
        assignments = validated_data.get('assignments', [])

        if not assignments:
            raise serializers.ValidationError({"assignments": "No assignments provided."})

        updated_instances = []

        for item in assignments:
            teacher_name = item.get('teacher')
            role = item.get('role')

            try:
                teacher = Instructor.objects.get(name__iexact=teacher_name)
            except Instructor.DoesNotExist:
                raise serializers.ValidationError({"teacher": f"Instructor '{teacher_name}' does not exist"})

        obj, created = AssignClassTeacher.objects.update_or_create(
            classroom=classroom,
            section=section,
            teacher=teacher,
            defaults={"role": role}
        )

        updated_instances.append({
            "teacher": teacher_name,
            "role": role,
            "status": "created" if created else "updated"
        })

        return {
            "classroom": classroom.id,
            "section": section.id,
            "assignments": updated_instances
    }
