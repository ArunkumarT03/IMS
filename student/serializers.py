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
        try:
            
            request = self.context.get("request")
            if request is None:
                raise Exception("Request context missing")

            raw_password = request.data.get("password")
            if not raw_password:
                raise serializers.ValidationError({"password": "Password is required"})

            # Extract cls/sec
            cls = validated_data.pop("cls")
            sec = validated_data.pop("sec")

            # Find or create classroom
            classroom, created = ClassRoom.objects.get_or_create(
                 cls=cls.strip(),
                 sec=sec.strip()
            )

            # Create user
            email = validated_data.get("email")
            user = User.objects.create_user(
                email=email,
                password=raw_password,
                role="student"
            )

            # Create student
            student = Student.objects.create(
                user=user,
                classroom=classroom,
                **validated_data
            )

            return student
        except Exception as e:
             raise serializers.ValidationError({"error": str(e)})