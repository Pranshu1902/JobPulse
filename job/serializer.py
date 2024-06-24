from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Job, JobStatusUpdate, JobComment, Company, CustomUserModel


class CustomUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ["userId", "username", "email", "password"]

    def create(self, validated_data):
        user = CustomUserModel.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"],
        )

        return user


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "username", "email", "password", "first_name", "last_name"]
#         read_only_fields = ["password"]


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
    comments = serializers.SerializerMethodField()
    statuses = serializers.SerializerMethodField()
    company = CompanySerializer(read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ["applicant"]

    def get_comments(self, obj):
        comments = obj.comments.order_by("-date")
        return JobCommentSerializer(comments, many=True).data

    def get_statuses(self, obj):
        statuses = obj.statuses.order_by("-date_posted")
        return JobStatusUpdateSerializer(statuses, many=True).data

    def get_status(self, obj):
        latest_status = obj.statuses.order_by("-date_posted").first()
        if latest_status:
            return JobStatusUpdateSerializer(latest_status).data
        return None
