from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers
from apps.snippets import views

urlpatterns = [
    path('snippets/v1/', views.snippet_list_v1),
    path('snippets/v1/<int:pk>/', views.snippet_detail_v1),
    path('snippets/v2/', views.snippet_list_v2),
    path('snippets/v2/<int:pk>/', views.snippet_detail_v2),

    path('snippets/v3/', views.SnippetListV3.as_view()),
    path('snippets/v3/<int:pk>/', views.SnippetDetailV3.as_view()),
    path('snippets/v5/', views.SnippetListV5.as_view()),
    path('snippets/v5/<int:pk>/', views.SnippetDetailV5.as_view()),

    path('snippets/users/', views.UserList.as_view()),
    path('snippets/users/<int:pk>/', views.UserDetail.as_view()),
]

#
# Hyperlink
#

if False:
    urlpatterns += format_suffix_patterns([
        path('snippets/', views.api_root),
        path('hyperlink/snippets/',
             views.SnippetListV4.as_view(),
             name='snippet-list'),
        path('hyperlink/snippets/<int:pk>/',
             views.SnippetDetailV4.as_view(),
             name='snippet-detail'),
        path('hyperlink/snippets/<int:pk>/highlight/',
             views.SnippetHighlight.as_view(),
             name='snippet-highlight'),

        path('hyperlink/users/',
             views.UserList.as_view(),
             name='user-list'),
        path('hyperlink/users/<int:pk>/',
             views.UserDetail.as_view(),
             name='user-detail')
    ])


#
# Viewset
#

if True:
    snippet_list = views.SnippetViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })
    snippet_detail = views.SnippetViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })
    snippet_highlight = views.SnippetViewSet.as_view({
        'get': 'highlight'
    }, renderer_classes=[renderers.StaticHTMLRenderer])
    user_list = views.UserViewSet.as_view({
        'get': 'list'
    })
    user_detail = views.UserViewSet.as_view({
        'get': 'retrieve'
    })

    urlpatterns += format_suffix_patterns([
        path('snippets/', views.api_root),
        path('viewset/snippets/', snippet_list, name='snippet-list'),
        path('viewset/snippets/<int:pk>/',
             snippet_detail, name='snippet-detail'),
        path('viewset/snippets/<int:pk>/highlight/',
             snippet_highlight, name='snippet-highlight'),
        path('viewset/users/', user_list, name='user-list'),
        path('viewset/users/<int:pk>/', user_detail, name='user-detail')
    ])
