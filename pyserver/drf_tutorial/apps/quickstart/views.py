import datetime
from datetime import datetime as dt

from django.contrib.auth.models import User, Group
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import permissions
from rest_framework import serializers as rft_serializers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.quickstart import models
from apps.quickstart import serializers
from apps.quickstart import filtersets


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class PersonViewSet(viewsets.ModelViewSet):
    queryset = models.Person.objects.all().order_by('age')
    serializer_class = serializers.PersonSerializer

    def get_serializer_class(self):
        if self.action == 'by_filter':
            return serializers.PersonFilterSerializer
        return self.serializer_class

    @action(detail=False, methods=['POST'])
    def by_filter(self, request: Request, *args, **kwargs) -> Response:
        # post data validation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        role = data['role']
        age = data['age']
        persons = self.get_queryset().filter(role=role, age__lte=age).values()
        serializer = self.serializer_class(persons, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def by_birthday_range(self, request: Request, *args, **kwargs) -> Response:
        # query params validation
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        if not start or not end:
            raise rft_serializers.ValidationError(
                'Parameter [start] or [end] cannot be empty.')

        # filter by birthday range
        formater = '%Y-%m-%d'
        startdate = dt.strptime(start, formater)
        enddate = dt.strptime(end, formater)
        presons = self.queryset.filter(
            birthday__range=[startdate, enddate]).values()
        serializer = self.get_serializer(presons, many=True)
        return Response(serializer.data)


class CourseFreeList(generics.ListAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = filtersets.CoursePriceFilterSet
