FROM python:latest

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

ENV DATABASE_URL db_URL
ENV PORT 8000
ENV SSL "TRUE"

EXPOSE $PORT

COPY . .

ENTRYPOINT Scripts/run.sh