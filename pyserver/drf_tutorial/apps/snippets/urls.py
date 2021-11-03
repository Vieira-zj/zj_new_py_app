from django.urls import path, include
from apps.snippets import views

urlpatterns = [
    path('snippets/v1/', views.snippet_list_v1),
    path('snippets/v1/<int:pk>/', views.snippet_detail_v1),
    path('snippets/v2/', views.snippet_list_v2),
    path('snippets/v2/<int:pk>/', views.snippet_detail_v2),

    path('snippets/v3/', views.SnippetListV3.as_view()),
    path('snippets/v3/<int:pk>/', views.SnippetDetailV3.as_view()),
    path('snippets/v4/', views.SnippetListV4.as_view()),
    path('snippets/v4/<int:pk>/', views.SnippetDetailV4.as_view()),
    path('snippets/v5/', views.SnippetListV4.as_view()),
    path('snippets/v5/<int:pk>/', views.SnippetDetailV5.as_view()),

    path('snippets/users/', views.UserList.as_view()),
    path('snippets/users/<int:pk>/', views.UserDetail.as_view()),
]
