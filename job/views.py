from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .serializer import *
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet): #GenericViewSet, mixins.CreateModelMixin):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    @action(detail=True, methods=['GET'], serializer_class=JobStatusUpdateSerializer)
    def get_status(self, request, *args):
        job = self.get_object()
        statuses = job.statuses.all()
        serializer = self.get_serializer(statuses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], serializer_class=JobCommentSerializer)
    def get_comments(self, request, *args):
        job = self.get_object()
        statuses = job.comments.all()
        serializer = self.get_serializer(statuses, many=True)
        return Response(serializer.data)


class JobStatusUpdateViewSet(viewsets.ModelViewSet):
    queryset = JobStatusUpdate.objects.all()
    serializer_class = JobStatusUpdateSerializer


class JobCommentViewSet(viewsets.ModelViewSet):
    queryset = JobComment.objects.all()
    serializer_class = JobCommentSerializer
