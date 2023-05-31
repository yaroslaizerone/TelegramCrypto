#!/bin/bash
apt-get -y update
apt-get -y install python3-pip python3.10-venv postgresql postgresql-contrib libpq-dev python3-dev gcc celery systemd redis-server
python3 -m venv /home/vagrant/.venv
source /home/vagrant/.venv/bin/activate
pip install redis Django psycopg2 flower
pip install -r /home/vagrant/calldb/requirements.txt
sudo -u postgres psql \
-c "CREATE DATABASE test_db;" \
-c "CREATE USER yarik WITH ENCRYPTED PASSWORD '1234';" \
-c "ALTER ROLE yarik SET client_encoding TO 'utf8';" \
-c "ALTER ROLE yarik SET default_transaction_isolation TO 'read committed';" \
-c "ALTER ROLE yarik SET timezone TO 'UTC';" \
-c "GRANT ALL PRIVILEGES ON DATABASE test_db TO yarik;"
python /home/vagrant/calldb/web/manage.py migrate --skip-checks
DJANGO_SUPERUSER_USERNAME=yarik DJANGO_SUPERUSER_EMAIL=gmail@gmail.com DJANGO_SUPERUSER_PASSWORD=1234 \
python /home/vagrant/calldb/web/manage.py createsuperuser --no-input
sudo cp calldb/systemd.servise/celery.service calldb/systemd.servise/celeryflower.service /etc/systemd/system/