#! /bin/bash
python manage.py migrate
python manage.py set_superuser --username $ADMIN_USERNAME --password $ADMIN_PASSWORD
python manage.py collectstatic --noinput
python manage.py compilemessages

exec uwsgi --ini /uwsgi.ini
