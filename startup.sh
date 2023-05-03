\#!/bin/bash
pip install -r requirements.txt
gnome-terminal --tab --title="Celery" --command="bash -c 'celery -A app.celery worker --loglevel=info'"
gunicorn --bind=0.0.0.0 --workers=4  app:app --timeout=600