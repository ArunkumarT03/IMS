from rest_framework import serializers
from users.models import *
from student.models import *

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "name", "fathername", "dob", "gender",
            "phone", "email", "cls", "sec"
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        if request is None:
            raise Exception("Request context missing")

        raw_password = request.data.get("password")
        if not raw_password:
            raise serializers.ValidationError({"password": "Password is required"})

        email = validated_data.get("email")

        user = User.objects.create_user(
            email=email,
            password=raw_password,
            role="student"
        )

        student = Student.objects.create(
            user=user,
            **validated_data
        )

        return student