from django.contrib.auth.models import User
from rest_framework import serializers
from apps.snippets.models import Snippet


class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos',
                  'language', 'style', 'owner']


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']

#
# Hyperlink
#


class HyperlinkSnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # point to "snippet-highlight" url pattern
    highlight = serializers.HyperlinkedIdentityField(
        view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        # url point to "snippet-detail" url pattern
        fields = ['url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style']


class HyperlinkUserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(
        many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']

#
# Test
#


def test_user_serializer():
    ser = UserSerializer()
    print(repr(ser))

    user = User.objects.get(id=1)
    ser = UserSerializer(user)
    print(ser.data)


def test_user_serializer_save():
    import json
    # when add user by set "snippets" ids, it will sync data in snippets table
    content = '{"username": "bar", "email": "bar@test.com", "is_active": false, "snippets": []}'
    data = json.loads(content)
    ser = UserSerializer(data=data)
    ser.is_valid(raise_exception=True)
    ser.save()
    print('user count:', User.objects.count())


def test_snippet_serializer():
    snippet = Snippet.objects.get(id=1)
    ser = SnippetSerializer(snippet)
    print(ser.data)

    sers = SnippetSerializer(Snippet.objects.all(), many=True)
    for ser in sers.data:
        print(ser)


def test_snippet_serializer_save():
    import json
    content = '{"title": "Foo", "code": "print(\\"hello, world\\")\\n", "linenos": false, "language": "python", "style": "friendly"}'
    data = json.loads(content)
    ser = SnippetSerializer(data=data)
    ser.is_valid(raise_exception=True)
    admin = User.objects.get(username='admin')
    ser.save(owner=admin)  # save by set foreign key
    print('count:', Snippet.objects.count())
