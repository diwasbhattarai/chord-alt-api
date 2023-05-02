\#!/bin/bash
apt-get -y install ffmpeg
apt-get -y install supervisor
mkdir /var/log/celery/
cp supervisord.conf /etc/supervisor/conf.d/
supervisorctl reread
supervisorctl update
supervisord
gunicorn  -w 1 --threads 12 --bind '0.0.0.0:8000' app:server --timeout 30