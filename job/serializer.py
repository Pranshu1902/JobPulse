from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Job, JobStatusUpdate, JobComment

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class JobSerializer(serializers.Serializer):
    class Meta:
        model = Job
        fields = '__all__'


class JobStatusUpdateSerializer(serializers.Serializer):
    class Meta:
        model = JobStatusUpdate
        fields = '__all__'


class JobCommentSerializer(serializers.Serializer):
    class Meta:
        model = JobComment
        fields = '__all__'
