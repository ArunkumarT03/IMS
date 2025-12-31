from rest_framework import serializers
from .models import*
from Academics.models import*
from users.models import*

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['subject_name', 'subject_code']


class InstructorSerializer(serializers.ModelSerializer):
    subject_ids = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        many=True,
        write_only=True,
        source="subjects"
    )
    subjects = SubjectSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True,required=False,allow_blank=True)
    email = serializers.EmailField()   # <-- Now using Instructor.email

    class Meta:
        model = Instructor
        fields = [  
            "id",
            "name",
            "email",
            "phone",
            "qualification",
            "experience",
            "subjects",
            "subject_ids",
            "password",
        ]

    def create(self, validated_data):
        subjects = validated_data.pop("subjects", [])
        raw_password = validated_data.pop("password")

        # email now comes from Instructor model
        email = validated_data.get("email")

        if not email:
            raise serializers.ValidationError({"email": "Email is required"})

        # Create User (using the instructor's email)
        user = User.objects.create_user(
            email=email,
            password=raw_password,
            role="instructor"
        )

        # Create Instructor linked to the User
        instructor = Instructor.objects.create(user=user, **validated_data)

        # Add ManyToMany
        instructor.subjects.set(subjects)

        return instructor


    def update(self, instance, validated_data):
        subjects = validated_data.pop("subjects", None)
        password = validated_data.pop("password", None)
        email = validated_data.pop("email", None)

        # ✅ Update Instructor fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # ✅ Update email in BOTH Instructor & User
        if email:
            instance.email = email
            if instance.user:
                instance.user.email = email
                instance.user.save()

        # ✅ Update password
        if password and instance.user:
            instance.user.set_password(password)
            instance.user.save()

        # ✅ Update subjects
        if subjects is not None:
            instance.subjects.set(subjects)

        instance.save()
        return instance
    
class SubjectMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'subject_name', 'subject_code']


class InstructorSubjectsSerializer(serializers.ModelSerializer):
    subjects = SubjectMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Instructor
        fields = ['id', 'name', 'subjects']

class InstructorSubjectsUpdateSerializer(serializers.Serializer):
    subject_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )

    def update(self, instance, validated_data):
        subject_ids = validated_data.get('subject_ids', [])
        subjects = Subject.objects.filter(id__in=subject_ids)

        if subjects.count() != len(subject_ids):
            existing_ids = set(subjects.values_list('id', flat=True))
            missing = set(subject_ids) - existing_ids
            raise serializers.ValidationError(
                {"subject_ids": f"Subjects not found: {', '.join(map(str, missing))}"}
            )

        instance.subjects.set(subjects)
        instance.save()
        return instance