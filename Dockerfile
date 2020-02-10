FROM python:3.8.1-slim

COPY src /comments

WORKDIR /comments

RUN pip install --no-cache-dir -r requirements.txt

CMD ["/bin/sh", "run_gunicorn.sh"]
