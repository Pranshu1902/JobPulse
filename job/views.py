from django.shortcuts import render
from rest_framework import serializers, viewsets
from django.contrib.auth.models import User

# Create your views here.
class UserSerializer(serializers.Serializer):
    class Meta:
        fields = ('username', 'email')
        model = User


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
