# Django Rest Framework Tutorial

> Refer: Django模型 <https://docs.djangoproject.com/zh-hans/3.1/topics/db/>
>

## Quick Start

> Refer: <https://www.django-rest-framework.org/tutorial/quickstart/>
>

### Setup

1. Project setup

```sh
django-admin startproject drf_tutorial .
```

2. Dir `config/` Setup, and update `manage.py` and `setting.py`

3. App setup

```sh
django-admin startapp quickstart ./apps/quickstart
```

Sync `INSTALLED_APPS` in `setting.py`.

4. Sync database

```sh
python manage.py migrate
```

5. Create an initial user with pwd `password123`

```sh
python manage.py createsuperuser --email admin@example.com --username admin
```

### Server Up and Test

1. Run server

```sh
python manage.py runserver
```

2. Test api

```sh
# without auth
curl -H 'Accept:application/json' http://127.0.0.1:8000/users/ | jq .
# invalid pwd
curl -H 'Accept:application/json' -u admin:password http://127.0.0.1:8000/users/ | jq .
# ok
curl -H 'Accept:application/json' -u admin:password123 http://127.0.0.1:8000/users/ | jq .
```

------

## Tutorial

> Refer: <https://www.django-rest-framework.org/tutorial/1-serialization/>
>

### Setup

1. App setup

```sh
python manage.py startapp snippets ./apps/snippets
```

2. Create model and run initial migration

```sh
# create migrate script in dir "migrations/"
python manage.py makemigrations snippets
# migration to db
python manage.py migrate
```

3. Create serializer and view

4. Start up server

```sh
python manage.py runserver
```

5. Test api

```sh
# create
curl -XPOST http://127.0.0.1:8000/snippets/v5/ \
  -H 'Content-Type:application/json' -H 'Accept:application/json' \
  -d '{ "title": "", "code": "foo = \"bar\"\n", "linenos": false, "language": "python", "style": "friendly" }'
curl -XPOST http://127.0.0.1:8000/snippets/v5/ \
  -H 'Content-Type:application/json' -H 'Accept:application/json' \
  -d '{ "title": "", "code": "print(\"hello, world\")\n", "linenos": false, "language": "python", "style": "friendly" }'

# list
curl http://127.0.0.1:8000/snippets/v5/ | jq .
# get
curl http://127.0.0.1:8000/snippets/v5/2/ | jq .

# delete
curl -XDELETE http://127.0.0.1:8000/snippets/v5/1/ | jq .
```

> Note: if post data is json, it must set request format by header `Content-Type:application/json`, since the default value is form.
>

### Auth and Permssion

1. Rebuild database

```sh
rm -f db.sqlite3
rm -r apps/snippets/migrations
python manage.py makemigrations snippets
python manage.py migrate
```

2. Test models and serializers

```text
py manage.py shell
> from apps.snippets import models
> models.select_admin_snippet_data()
> from apps.snippets import serializers
> serializers.test_snippet_serializer_save()
```

3. Test auth api

```sh
# invalid pwd
curl -XPOST http://127.0.0.1:8000/snippets/v5/ -u admin:password \
  -H 'Content-Type:application/json' -H 'Accept:application/json' \
  -d '{ "title": "", "code": "foo = \"bar\"\n", "linenos": false, "language": "python", "style": "friendly" }'

# ok
curl -XPOST http://127.0.0.1:8000/snippets/v5/ -u admin:password123 \
  -H 'Content-Type:application/json' -H 'Accept:application/json' \
  -d '{ "title": "", "code": "foo = \"bar\"\n", "linenos": false, "language": "python", "style": "friendly" }'
```

4. Test custom object permissions

```sh
# by pass for GET
curl -u foo:bar http://127.0.0.1:8000/snippets/v5/35/ | jq .

# failed by request.user != owner
# "You do not have permission to perform this action."
curl -XDELETE -u foo:bar http://127.0.0.1:8000/snippets/v5/35/ | jq .
# ok
curl -XDELETE -u admin:password123 http://127.0.0.1:8000/snippets/v5/35/ | jq .
````

### Hyperlinked API

It improves discoverability of API, by instead using hyperlinking for relationships.

In chrome, open url <http://127.0.0.1:8000/snippets/>.

### Viewsets

Test viewsets api:

```sh
# retrieve
curl http://127.0.0.1:8000/viewset/snippets/ | jq .
curl http://127.0.0.1:8000/viewset/snippets/38/ | jq .
curl http://127.0.0.1:8000/viewset/snippets/38/highlight/ | jq .

# delete
# failed: "You do not have permission to perform this action."
curl -XDELETE -u test:1 http://127.0.0.1:8000/viewset/snippets/38/ | jq .
# ok
curl -XDELETE -u admin:password123 http://127.0.0.1:8000/viewset/snippets/38/ | jq .

# create
curl -XPOST http://127.0.0.1:8000/viewset/snippets/ -u admin:password123 \
  -H 'Content-Type:application/json' -H 'Accept:application/json' \
  -d '{ "title": "", "code": "foo = \"bar\"\n", "linenos": false, "language": "python", "style": "friendly" }'
```

------

## Diango External

### ForeignKey

Build db schema:

```sh
python manage.py makemigrations
python manage.py migrate
```

Run test:

```text
py manage.py shell
> from apps.quickstart import models
> models.get_all_female_student()
```

### Serializer Validation

1. Create models, serializers and views.

2. Test api

```sh
# create
curl -XPOST http://127.0.0.1:8000/quickstart/person/  \
  -H 'Content-Type:application/json' -H 'Accept:application/json' \
  -d '{ "name": "foo", "age": 33, "birthday": "1983-7-1", "role": "qa", "language": "python" }'

# retrieve
curl http://127.0.0.1:8000/quickstart/person/ | jq .
curl http://127.0.0.1:8000/quickstart/person/1/ | jq .

# delete
curl -XDELETE http://127.0.0.1:8000/quickstart/person/3/ | jq .

# search
# get filter results by post
curl "http://127.0.0.1:8000/quickstart/person/by-filter/" \
  -H 'Content-Type:application/json' -H 'Accept:application/json' \
  -d '{ "role": "qa", "age": 30 }' | jq .
# get by date range
curl "http://127.0.0.1:8000/quickstart/person/by-filter/?start=1980-1-1&end=1986-12-10" | jq .
```

### FilterSet

Create `CoursePriceFilterSet`, and set `filter_backends` and `filter_class` in view. Test by diff prices:

```sh
curl "http://127.0.0.1:8000/courses/free/?max_price=400" | jq .
curl -H 'Accept:application/json' "http://127.0.0.1:8000/courses/free/?max_price=600" | jq .
```

