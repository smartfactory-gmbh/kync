#!/usr/bin/env sh

# Use wrapper script to wait until postgres accepts tcp connections
# Resource: https://docs.docker.com/compose/startup-order/
chmod +x ./.docker/wait-for
./.docker/wait-for $POSTGRES_HOST:5432
echo '[*] DB is up and running'

python manage.py migrate

# Uncomment the following if you use i18n
#python manage.py compilemessages
