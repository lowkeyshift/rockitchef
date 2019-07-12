#!/bin/sh
#sleep 3
#python3 manage.py makemigrations
#python3 manage.py migrate
#python3 manage.py collectstatic
#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input --clear
python manage.py auto_createsuper --email 'admin@rockitchef.com' --password 123rockit321 --noinput
gunicorn rockitchef_project.wsgi:application --bind 0.0.0.0:8000
exec "$@"
