FROM python:latest

WORKDIR /app

COPY . .

ENV DATABASE_URL db_URL

RUN pip install -r requirements.txt

CMD [ "gunicorn application:app --preload" ]