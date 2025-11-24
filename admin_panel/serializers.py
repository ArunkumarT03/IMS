from rest_framework import serializers
from admin_panel.models import *
from users.serializers import *

class AdminSignupSerializer(serializers.ModelSerializer):
    # these fields will come in request
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Admin_panel
        fields = ["email", "password"]

    def create(self, validated_data):
        email = validated_data.pop("email")
        raw_password = validated_data.pop("password")

        # 1️⃣ Create User
        user = User.objects.create_user(
            email=email,
            password=raw_password,
            role="admin"    # auto-set role
        )

        # 2️⃣ Create Admin Profile
        admin_profile = Admin_panel.objects.create(
            user=user,
            **validated_data
        )

        return admin_profile