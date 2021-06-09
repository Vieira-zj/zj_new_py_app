# Django Rest Framework

Refer:

- Quick start: <https://www.django-rest-framework.org/tutorial/quickstart/>
- Github: <https://github.com/encode/rest-framework-tutorial>
- Django模型 <https://docs.djangoproject.com/zh-hans/3.1/topics/db/>

## Quickstart

### Project setup

Create a new Django project named `tutorial`, then start a new app called `quickstart`.

```sh
# Install Django and Django REST framework into the virtual environment
pip install django
pip install djangorestframework

# Set up a new project with a single application
django-admin startproject tutorial .  # Note the trailing '.' character
cd tutorial
django-admin startapp quickstart
cd ..
```

Sync your database for the first time:

```sh
python manage.py migrate
```

Create an initial user named `admin` with a password of `password123`.

```sh
python manage.py createsuperuser --email admin@example.com --username admin
```

Query the `db.sqlite3`:

```text
.show
.headers on
.mode column
.timer on

.tables
.schema auth_user
.quit

select * from auth_user;
```

### Testing our API

Fire up the server from the command line.

```sh
python manage.py runserver
```

Test:

```sh
curl -H 'Accept: application/json; indent=4' -u admin:password123 http://127.0.0.1:8000/users/
```

## Tutorial 1: Serialization

Setting up a new environment.

```sh
pip install django
pip install djangorestframework
pip install pygments
```

Getting started.

```sh
django-admin startproject tutorial
cd tutorial
python manage.py startapp snippets
```

Create an initial migration for our snippet model, and sync the database for the first time.

```sh
python manage.py makemigrations snippets
python manage.py migrate
```

Start up Django's development server.

```sh
cd djangodemo/tutorial
python manage.py runserver
```

### Test

- Create records

```sh
curl -v -XPOST -H "Content-Type:application/json" http://127.0.0.1:8000/snippets/ -d @data.json
```

Json data:

```json
{"id": 1, "title": "", "code": "foo = \"bar\"", "linenos": false, "language": "python", "style": "friendly"}
{"id": 2, "title": "", "code": "print(\"hello, world\")", "linenos": false, "language": "python", "style": "friendly"}
```

- Retrieve records

```sh
curl -v http://127.0.0.1:8000/snippets/ | jq .
curl -v http://127.0.0.1:8000/snippets/2/ | jq .
```

- Delete record

```sh
curl -v -XDELETE http://127.0.0.1:8000/snippets/1/ | jq .
```

## Tutorial 2: Requests and Responses

Test:

```sh
curl -v http://127.0.0.1:8000/snippets/ | jq .
```

Control the format of the response that we get back, either by using the Accept header:

```sh
curl -v -H "Content-Type:application/json" -H "Accept:application/json" http://127.0.0.1:8000/snippets/ | jq .
curl -v -H "Content-Type:application/json" -H "Accept:text/html" http://127.0.0.1:8000/snippets/
```

Or by appending a format suffix:

```sh
curl -v http://127.0.0.1:8000/snippets.json | jq .
curl -v http://127.0.0.1:8000/snippets.api
```

## Tutorial 4: Authentication & Permissions

- Code snippets are always associated with a creator.
- Only authenticated users may create snippets.
- Only the creator of a snippet may update or delete it.
- Unauthenticated requests should have full read-only access.

Update our database tables.

```sh
rm -f db.sqlite3
rm -r snippets/migrations
python manage.py makemigrations snippets
python manage.py migrate
```

Create a few different users, to use for testing the API.

```sh
python manage.py createsuperuser --email admin@example.com --username admin
```

### Test

- auth

```text
http://127.0.0.1:8000/api-auth/login/
```

- Create records

```sh
curl -v -XPOST -H "Content-Type:application/json" -u admin:1234 http://127.0.0.1:8000/snippets/ -d @data.json
```

Json data:

```json
{"id": 1, "owner": "root", "title": "foo", "code": "print(789)", "linenos": false, "language": "python", "style": "friendly"}
```

- Retrieve records

```sh
curl -v http://127.0.0.1:8000/snippets/ | jq .
```

- Delete record

```sh
curl -XDELETE -v -u root:1234 http://127.0.0.1:8000/snippets/1/ | jq .
```

## Tutorial 5: Relationships & Hyperlinked APIs

1. The root of our API refers to 'user-list' and 'snippet-list'.

```sh
curl -v http://127.0.0.1:8000
```

Result json:

```json
{
    "users": "http://127.0.0.1:8000/users/",
    "snippets": "http://127.0.0.1:8000/snippets/"
}
```

2. Our snippet serializer includes a field that refers to 'snippet-highlight'.
3. Our user serializer includes a field that refers to 'snippet-detail'.
4. Our snippet and user serializers include 'url' fields that by default will refer to '{model_name}-detail', which in this case will be 'snippet-detail' and 'user-detail'.

Request snippets:

```sh
curl -v http://127.0.0.1:8000/snippets/ | jq .
# open in browser: http://127.0.0.1:8000/snippets/1/highlight/
```

Result json:

```json
{
    "url": "http://127.0.0.1:8000/snippets/1/",
    "id": 1,
    "highlight": "http://127.0.0.1:8000/snippets/1/highlight/",
    "owner": "admin",
    "title": "foo",
    "code": "print(789)",
    "linenos": false,
    "language": "python",
    "style": "friendly"
}
```

Request users:

```sh
curl -v http://127.0.0.1:8000/users/ | jq .
# open in browser http://127.0.0.1:8000/snippets/1/
```

Result json:

```json
{
    "url": "http://127.0.0.1:8000/users/1/",
    "id": 1,
    "username": "admin",
    "snippets": [
        "http://127.0.0.1:8000/snippets/1/",
        "http://127.0.0.1:8000/snippets/2/"
    ]
}
```

