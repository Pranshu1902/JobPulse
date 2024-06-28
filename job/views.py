from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from django.contrib.auth.models import User
from .serializer import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import render
from rest_framework.authtoken.models import Token


def index(request):
    return render(request, "home.html")


def usersCount(request):
    total_users = User.objects.count()
    return render(request, "users.html", {"total_users": total_users})


@api_view(http_method_names=["GET"])
def get_current_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):  # GenericViewSet, mixins.CreateModelMixin):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        method="post",
        request_body=UserSerializer,
        responses={201: UserSerializer, 400: "Bad Request"},
    )
    @action(detail=False, methods=["post"], permission_classes=[])
    def social_login(self, request, pk=None):
        try:
            # search for existing user
            existing_user = User.objects.get(username=request.data.get("username"))
            serializer = UserSerializer(existing_user)
            token, created = Token.objects.get_or_create(user=existing_user)
            return Response({"user": serializer.data, "token": token.key}, status=201)
        except:
            # create new user
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                token, created = Token.objects.get_or_create(user=serializer.save())
                return Response(
                    {"user": serializer.data, "token": token.key}, status=201
                )


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_queryset(self):
        queryset = Job.objects.filter(applicant=self.request.user).order_by(
            "-application_date"
        )
        return queryset

    def perform_destroy(self, instance):
        if instance.applicant != self.request.user:
            raise PermissionError("You can only delete jobs you created")
        instance.delete()

    def perform_update(self, serializer):
        job = self.get_object()
        if job.applicant != self.request.user:
            raise PermissionError("You can only update jobs you created")
        serializer.save()

    def perform_create(self, serializer):
        company_name = self.request.data.get("company")

        # search for existing company object with same name
        try:
            company = Company.objects.get(name=company_name)
        except Company.DoesNotExist:
            company = Company.objects.create(name=company_name)

        job = serializer.save(applicant=self.request.user, company=company)

        # Automatically create a default Job Status for this job
        status_data = {
            "status": "Applied",
            "update_text": "Initialize Job",
        }
        status_serializer = JobStatusUpdateSerializer(data=status_data)
        if status_serializer.is_valid():
            status_serializer.save(job=job)
        else:
            raise serializers.ValidationError(status_serializer.errors)

    @swagger_auto_schema(
        method="post",
        request_body=JobCommentSerializer,
        responses={201: JobCommentSerializer, 400: "Bad Request"},
    )
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def comment(self, request, pk=None):
        job = self.get_object()

        if job.applicant.id != self.request.user.id:
            raise PermissionDenied("You do not have permission to perform this action")

        serializer = JobCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(job=job)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        method="post",
        request_body=JobStatusUpdateSerializer,
        responses={201: JobStatusUpdateSerializer, 400: "Bad Request"},
    )
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def update_status(self, request, pk=None):
        job = self.get_object()

        if job.applicant.id != self.request.user.id:
            raise PermissionDenied("You do not have permission to perform this action")

        serializer = JobStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(job=job)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(method="get", responses={200: JobStatusUpdateSerializer})
    @action(detail=True, methods=["GET"], serializer_class=JobStatusUpdateSerializer)
    def get_current_status(self, request, pk=None, *args):
        job = self.get_object()
        latest_status = job.statuses.order_by("-date_posted").first()
        serializer = self.get_serializer(latest_status)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"], serializer_class=JobStatusUpdateSerializer)
    def get_all_status(self, request, *args):
        job = self.get_object()
        statuses = job.statuses.all().order_by("-date_posted")
        serializer = self.get_serializer(statuses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"], serializer_class=JobCommentSerializer)
    def get_all_comments(self, request, pk=None):
        job = self.get_object()
        comments = job.comments.all().order_by("-date")
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)


class JobStatusUpdateViewSet(viewsets.ModelViewSet):
    queryset = JobStatusUpdate.objects.all()
    serializer_class = JobStatusUpdateSerializer

    def perform_destroy(self, instance):
        if instance.job.applicant != self.request.user:
            raise PermissionError("You can only delete jobs you created")
        instance.delete()

    def perform_update(self, serializer):
        status_update = self.get_object()
        if status_update.job.applicant != self.request.user:
            raise PermissionError("You can only update jobs you created")
        serializer.save()


class JobCommentViewSet(viewsets.ModelViewSet):
    queryset = JobComment.objects.all()
    serializer_class = JobCommentSerializer

    def perform_destroy(self, instance):
        if instance.job.applicant != self.request.user:
            raise PermissionError("You can only delete jobs you created")
        instance.delete()

    def perform_update(self, serializer):
        job_comment = self.get_object()
        if job_comment.job.applicant != self.request.user:
            raise PermissionError("You can only update jobs you created")
        serializer.save()


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
