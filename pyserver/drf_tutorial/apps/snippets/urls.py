from django.urls import path
from pyserver.drf_tutorial.apps.snippets import views

urlpatterns = [
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail),
]
