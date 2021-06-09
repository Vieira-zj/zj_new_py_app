#!/bin/bash
set -e

function restore_db() {
    rm db.sqlite3
    rm -r snippets/migrations
    python manage.py makemigrations snippets
    python manage.py migrate
}

function start() {
    python manage.py runserver
}

if [[ $1 == "restore" ]]; then
    restore_db
fi

if [[ $1 == "start" ]]; then
    start
fi

echo "Done"
