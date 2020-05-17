# AGOL Data Filter

## Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- (if you don't have a database) [Docker Compose](https://docs.docker.com/compose/install/)

## Setup
### I have a PostgreSQL Database
Set the environment variable `DATABASE_URL` to the URL of your SQL database (preferably PostgreSQL), `PORT` to the port you want the application to listen on, and `SSL` to `TRUE` if your database requires an SSL connection, or `FALSE` otherwise. DO NOT append `?sslmode=require` to `DATABASE_URL`, this is done by the application, depending on the state of `SSL`.

### I don't have a PostgreSQL Database
Set the environment variable `PORT` to the port you want the application to listen on. Then go to [Run](#run).

## Run
### I have a PostgreSQL Database

#### Build
```bash
$ docker build --pull --rm -f "Dockerfile" -t agoldatafilter:latest "."
```

#### Run
```bash
$ docker run -e "DATABASE_URL=$DATABASE_URL" -e "PORT=$PORT" -e "SSL=$SSL" -p $PORT:$PORT -d agoldatafilter
```

#### Shutdown
```bash
$ docker kill $(docker ps -q)
```

### I don't have a PostgreSQL Database
#### Build
```bash
$ docker build --pull --rm -f "Dockerfile" -t agoldatafilter:latest "."
```

#### Run
```bash
$ docker-compose up
```