#!/bin/bash
$RUN_SCRIPT_PATH="/path/to/script.sh"
python manage.py migrate        # Apply database migrations
python manage.py collectstatic --clear --noinput # clearstatic files
python manage.py collectstatic --noinput  # collect static files
# Prepare log files and start outputting logs to stdout
touch /var/app/logs/gunicorn.log
touch /var/app/logs/access.log
tail -n 0 -f /var/app/logs/*.log &
echo Starting nginx
# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn cashApi.wsgi:application \
    --name cashApi \
    --bind unix:django_app.sock \
    --workers 3 \
    --log-level=info \
    --log-file=/var/app/logs/gunicorn.log \
    --access-logfile=/var/app/logs/access.log &
exec service nginx start
"$SCRIPT_PATH"
