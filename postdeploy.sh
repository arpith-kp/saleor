#!/bin/sh
python manage.py migrate
python manage.py populatedb
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser(email='admin@example.com', password='Password1')" | python manage.py shell
