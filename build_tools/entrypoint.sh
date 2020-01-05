#!/bin/bash
# Prepare log files and start outputting logs to stdout
mkdir logs
touch logs/gunicorn.log
touch logs/access.log
tail -n 0 -f logs/*.log &

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn3 wsgi:app \
    --name emailvalidator \
    --bind 0.0.0.0:8080 \
    --log-level=info \
    --log-file=logs/gunicorn.log \
    --access-logfile=logs/access.log
    