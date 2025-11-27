from rest_framework import serializers
from users.models import *
from student.models import *

class StudentSerializer(serializers.ModelSerializer):
    cls = serializers.CharField(write_only=True)
    sec = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = [
            "name", "fathername", "dob", "gender",
            "phone", "email", "cls", "sec"
        ]

    def create(self, validated_data):
        request = self.context.get("request")

        if request is None:
            raise serializers.ValidationError({"error": "Request context missing"})

        # Get password
        raw_password = request.data.get("password")
        if not raw_password:
            raise serializers.ValidationError({"password": "Password is required"})

        # Extract cls & sec
        cls_value = validated_data.pop("cls").strip()
        sec_value = validated_data.pop("sec").strip()

        # Create or get ClassRoom
        classroom, _ = ClassRoom.objects.get_or_create(
            cls=cls_value
        )

        # FIXED → correct field is cls, NOT classroom
        section, _ = Section.objects.get_or_create(
            cls=classroom,
            sec=sec_value
        )

        # Create User
        email = validated_data.get("email")
        user = User.objects.create_user(
            email=email,
            password=raw_password,
            role="student"
        )

        # Create Student record
        student = Student.objects.create(
            user=user,
            section=section,
            **validated_data
        )

        return student

