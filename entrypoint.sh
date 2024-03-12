#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python ./drone_management/manage.py collectstatic --no-input
python ./drone_management/manage.py migrate
python ./drone_management/manage.py makemigrations

DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD python ./drone_management/manage.py createsuperuser --username $SUPER_USER_NAME --email $SUPER_USER_EMAIL --noinput

python ./drone_management/manage.py runserver 0.0.0.0:8000

exec "$@"
