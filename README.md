# AGOL Data Filter

## Prerequisites
- [Docker](https://docs.docker.com/get-docker/)

## Setup
Set the environment variable `DATABASE_URL` to the URL of your SQL database (preferably PostgreSQL), and `PORT` to the port you want the application to listen on. DO NOT append `?sslmode=require` to `DATABASE URL`, this is done by the application.

## Run
### Build
```bash
$ docker build --pull --rm -f "Dockerfile" -t agoldatafilter:latest "."
```

### Run
```bash
$ docker run -e "DATABASE_URL=$DATABASE_URL" -e "PORT=$PORT" -p $PORT:$PORT -d agoldatafilter
```

### Shutdown
```bash
$ docker kill $(docker ps -q)
```