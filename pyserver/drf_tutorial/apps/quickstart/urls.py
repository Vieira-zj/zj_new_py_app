from django.urls import path, include
from rest_framework import renderers
from apps.quickstart import views

urlpatterns = [
    path('courses/free/', views.CourseFreeList.as_view()),
]
