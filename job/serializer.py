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
    statuses = serializers.SerializerMethodField()
    company = CompanySerializer(read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ["applicant"]

    def get_statuses(self, obj):
        statuses = obj.statuses.order_by("-date_posted")
        return JobStatusUpdateSerializer(statuses, many=True).data

    def get_status(self, obj):
        latest_status = obj.statuses.order_by("-date_posted").first()
        if latest_status:
            return JobStatusUpdateSerializer(latest_status).data
        return None
