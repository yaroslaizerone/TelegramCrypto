#!/bin/bash
apt-get -y update
apt-get -y install python3-pip python3.10-venv postgresql postgresql-contrib libpq-dev python3-dev gcc celery systemd redis-server
python3 -m venv /home/vagrant/test_django_project/.venv
source /home/vagrant/test_django_project/.venv/bin/activate
pip install redis Django psycopg2 flower
sudo -u postgres psql \
-c "CREATE DATABASE test_db;" \
-c "CREATE USER yarik WITH ENCRYPTED PASSWORD '1234';" \
-c "ALTER ROLE yarik SET client_encoding TO 'utf8';" \
-c "ALTER ROLE yarik SET default_transaction_isolation TO 'read committed';" \
-c "ALTER ROLE yarik SET timezone TO 'UTC';" \
-c "GRANT ALL PRIVILEGES ON DATABASE test_db TO yarik;"
python /home/vagrant/test_django_project/src/test_django_project/manage.py migrate
DJANGO_SUPERUSER_USERNAME=yarik DJANGO_SUPERUSER_EMAIL=gmail@gmail.com DJANGO_SUPERUSER_PASSWORD=1234 \
python /home/vagrant/test_django_project/src/test_django_project/manage.py createsuperuser --no-input