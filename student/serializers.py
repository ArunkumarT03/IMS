from rest_framework import serializers
from users.models import*
from student.models import*

class StudentSerializer(serializers.ModelSerializer):
    # For POST
    cls = serializers.CharField(write_only=True)
    sec = serializers.CharField(write_only=True)

    # For GET
    class_name = serializers.CharField(source="section.cls.cls", read_only=True)
    section_name = serializers.CharField(source="section.sec", read_only=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "name",
            "fathername",
            "dob",
            "gender",
            "phone",
            "email",
            "cls",
            "sec",
            "class_name",
            "section_name"
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        if not request:
            raise serializers.ValidationError({"error": "Request context missing"})

        # Password from request
        raw_password = request.data.get("password")
        if not raw_password:
            raise serializers.ValidationError({"password": "Password is required"})

        # Extract fields
        cls_value = validated_data.pop("cls").strip()
        sec_value = validated_data.pop("sec").strip()
        email = validated_data.get("email")

        # Create user
        user = User.objects.create_user(
            email=email,
            password=raw_password,
            role="student"
        )

        # Create classroom & section
        classroom, _ = ClassRoom.objects.get_or_create(cls=cls_value)
        section, _ = Section.objects.get_or_create(cls=classroom, sec=sec_value)

        # Create ONLY ONCE
        student = Student.objects.create(
            user=user,
            section=section,
            **validated_data
        )

        return student



