from rest_framework import serializers
from .models import*
from Academics.models import*
from users.models import*

class InstructorSerializer(serializers.ModelSerializer):
    subject_ids = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        many=True,
        write_only=True,
        source="subjects"
    )
    subjects = serializers.StringRelatedField(many=True, read_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Instructor
        fields = ["id", "name","email", "phone", "qualification", "experience",
                  "subjects", "subject_ids", "password"]

    def create(self, validated_data):
        subjects = validated_data.pop("subjects", [])
        raw_password = validated_data.pop("password")
        email = self.initial_data.get("email")  # get email from input data

        if not email:
            raise serializers.ValidationError({"email": "Email is required"})

        # Create User first
        user = User.objects.create_user(email=email, password=raw_password, role="instructor")

        # Create Instructor linked to user
        instructor = Instructor.objects.create(user=user, **validated_data)

        # Set ManyToMany subjects
        instructor.subjects.set(subjects)
        return instructor

    def update(self, instance, validated_data):
        subjects = validated_data.pop("subjects", None)
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.user.set_password(password)
            instance.user.save()

        if subjects is not None:
            instance.subjects.set(subjects)

        instance.save()
        return instance