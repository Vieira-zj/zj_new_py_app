from django.contrib.auth.models import User, Group
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from apps.quickstart.models import Course
from apps.quickstart.serializers import UserSerializer, GroupSerializer
from apps.quickstart.serializers import CourseSerializer
from apps.quickstart.filtersets import CoursePriceFilterSet


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseFreeList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = CoursePriceFilterSet
