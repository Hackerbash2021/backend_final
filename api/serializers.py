from rest_framework import serializers
from .models import (
    Organization,
    OrgClass,
    Exam,
    Student,
    OrgAdmin,
    UserClass
)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgAdmin
        fields = "__all__"


class OrgClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgClass
        fields = "__all__"


class Exam(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class UserClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserClass
        fields = "__all__"