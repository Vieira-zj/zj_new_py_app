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

2. Test API

```sh
curl -H 'Accept:application/json' http://127.0.0.1:8000/users/ | jq .
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

> Note: if post data is json, it must sets request format by header `Content-Type:application/json`, since the default value is form.
>

### Auth

1. Rebuild database

```sh
rm -f db.sqlite3
rm -r apps/snippets/migrations
python manage.py makemigrations snippets
python manage.py migrate
```

TODO:
