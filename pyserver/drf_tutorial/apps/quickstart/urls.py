from django.urls import path, include
from rest_framework import renderers
from apps.quickstart import views

urlpatterns = [
    path('courses/free/', views.CourseFreeList.as_view()),
]

person_list = views.PersonViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
person_detail = views.PersonViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
person_filter = views.PersonViewSet.as_view({
    'get': 'by_birthday_range',
    'post': 'by_filter'
})

urlpatterns += [
    path('quickstart/person/', person_list),
    path('quickstart/person/<int:pk>/', person_detail),
    path('quickstart/person/by-filter/', person_filter),
]
