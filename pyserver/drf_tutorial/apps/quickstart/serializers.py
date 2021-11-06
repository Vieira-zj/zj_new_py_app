from django.contrib.auth.models import User, Group
from rest_framework import serializers
from apps.quickstart import models

#
# User and Group
#


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

#
# Person
#


class PersonSerializer(serializers.ModelSerializer):
    # int转str, 方便前端处理
    id = serializers.CharField(required=False)

    class Meta:
        model = models.Person
        fields = ['id', 'name', 'age', 'birthday', 'role', 'language']


class PersonFilterSerializer(serializers.Serializer):
    age = serializers.IntegerField(required=True, min_value=23, max_value=50)
    role = serializers.CharField(required=True)

    def validate_role(self, value):
        if value.lower() not in ('dev', 'qa', 'manager'):
            raise serializers.ValidationError(
                f'Invalid person role value: {value}')
        return value

#
# Course
#


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['name', 'price']
