from django.contrib.auth.models import User
from django.http import Http404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import renderers
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from apps.snippets import models
from apps.snippets import serializers
from apps.snippets.permissions import IsOwnerOrReadOnly


@csrf_exempt
def snippet_list_v1(request):
    """
    List all code snippets, or create a new snippet.
    """
    # list all
    if request.method == 'GET':
        snippets = models.Snippet.objects.all()
        serializer = serializers.SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    # create
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=get_admin_user())
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def snippet_detail_v1(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = models.Smodels.nippet.objects.get(pk=pk)
    except models.Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = serializers.SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = serializers.SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)


@api_view(['GET', 'POST'])
def snippet_list_v2(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = models.Snippet.objects.all()
        serializer = serializers.SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = serializers.SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail_v2(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = models.Snippet.objects.get(pk=pk)
    except models.Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = serializers.SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#
# Class based view
# APIView
#


class SnippetListV3(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        snippets = models.Snippet.objects.all()
        serializer = serializers.SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetailV3(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return models.Snippet.objects.get(pk=pk)
        except models.Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = serializers.SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = serializers.SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#
# Mixins
#


class SnippetListV4(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset = models.Snippet.objects.all()
    serializer_class = serializers.HyperlinkSnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        print('request user:', self.request.user)
        serializer.save(owner=self.request.user)


class SnippetDetailV4(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    queryset = models.Snippet.objects.all()
    serializer_class = serializers.HyperlinkSnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

#
# Generics
#


class SnippetListV5(generics.ListCreateAPIView):
    queryset = models.Snippet.objects.all()
    serializer_class = serializers.SnippetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print('request user:', self.request.user)
        serializer.save(owner=self.request.user)


class SnippetDetailV5(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Snippet.objects.all()
    serializer_class = serializers.SnippetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

#
# User
#


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.HyperlinkUserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.HyperlinkUserSerializer

#
# Hyperlink
#


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format),
    })


class SnippetHighlight(generics.GenericAPIView):
    queryset = models.Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

#
# Viewset
#


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = models.Snippet.objects.all()
    serializer_class = serializers.SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

#
# Test
#


def get_admin_user():
    return User.objects.get(username='admin')
