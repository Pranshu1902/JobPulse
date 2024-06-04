from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Job, JobStatusUpdate, JobComment, Company


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"]
        )
        return user


class JobStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobStatusUpdate
        fields = "__all__"
        read_only_fields = ["id", "job", "date_posted"]


class JobCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobComment
        fields = "__all__"
        read_only_fields = ["job"]


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class JobSerializer(serializers.ModelSerializer):
    comments = JobCommentSerializer(many=True, read_only=True)
    statuses = JobStatusUpdateSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ["applicant"]
