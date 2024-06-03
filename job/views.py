from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from django.contrib.auth.models import User
from .serializer import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

@api_view(http_method_names=["GET"])
def get_current_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet): #GenericViewSet, mixins.CreateModelMixin):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)
        # TODO: automatically create a default Job Status for this job
    
    @swagger_auto_schema(
        method='post',
        request_body=JobCommentSerializer,
        responses={201: JobCommentSerializer, 400: 'Bad Request'}
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def comment(self, request, pk=None):
        job = self.get_object()
        serializer = JobCommentSerializer(data=request.data)
        if serializer.is_valid(): # and job.applicant == self.request.user ??
            # TODO: maybe add check that the authorized user is only performing the updation
            serializer.save(job=job)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    @swagger_auto_schema(
            method='post',
            request_body=JobStatusUpdateSerializer,
            responses={201: JobStatusUpdateSerializer, 400: 'Bad Request'}
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def update_status(self, request, pk=None):
        job = self.get_object()
        serializer = JobStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(job=job, user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['GET'], serializer_class=JobStatusUpdateSerializer)
    def get_current_status(self, request, *args):
        job = self.get_object()
        statuses = job.statuses.order_by('-date_posted').first()
        serializer = self.get_serializer(statuses, many=False)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], serializer_class=JobStatusUpdateSerializer)
    def get_all_status(self, request, *args):
        job = self.get_object()
        statuses = job.statuses.all()
        serializer = self.get_serializer(statuses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], serializer_class=JobCommentSerializer)
    def get_all_comments(self, request, *args):
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


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
