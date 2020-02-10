#/bin/sh

gunicorn -b 0.0.0.0:${FLASK_RUN_PORT} -w 2 app:app
