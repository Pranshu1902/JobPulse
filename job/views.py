# from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from django.contrib.auth.models import User
from .serializer import *
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet): #GenericViewSet, mixins.CreateModelMixin):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def create(self, request):
    #     print(request)
    #     if request.is_ajax():
    #         if request.method == 'POST':
    #             print(request.body)

    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobStatusUpdateViewSet(viewsets.ModelViewSet):
    queryset = JobStatusUpdate.objects.all()
    serializer_class = JobStatusUpdateSerializer


class JobCommentViewSet(viewsets.ModelViewSet):
    queryset = JobComment.objects.all()
    serializer_class = JobCommentSerializer
