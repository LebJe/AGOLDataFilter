FROM python:latest

WORKDIR /usr/src/app

COPY . .

ENV DATABASE_URL db_URL
ENV PORT 8000

RUN pip install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

EXPOSE $PORT

ENTRYPOINT Scripts/run.sh