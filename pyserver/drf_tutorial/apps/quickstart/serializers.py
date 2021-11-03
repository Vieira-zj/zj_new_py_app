from django.contrib.auth.models import User, Group
from rest_framework import serializers
from apps.quickstart import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['name', 'price']
