FROM python:latest

ENV DATABASE_URL DATABASE_URL

RUN pip install -r requirements.txt

RUN gunicorn application:app --preload