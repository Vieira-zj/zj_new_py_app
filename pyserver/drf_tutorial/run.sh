#!/bin/bash
set -ue

function clear_db() {
    local app='snippets'
    rm -f db.sqlite3
    rm -r apps/${app}/migrations
}

function build_db() {
    local app='snippets'
    python manage.py makemigrations ${app}
    python manage.py migrate
}

function runserver() {
    python manage.py runserver
}

# rebuild_db
runserver

echo 'django demo done'
