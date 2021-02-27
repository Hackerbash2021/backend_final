from rest_framework import serializers
from .models import (
    Organization,
    OrgClass,
    Exam,
    User,
    Admin,
)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = "__all__"


class OrgClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgClass
        fields = "__all__"


class Exam(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserClass
        fields = "__all__"