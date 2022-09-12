# _docker-compose.yaml_ Explained

```yaml

version: "3.9" #

services:
  app:
    build:  # build image from docker file.
      context: .  # path to the Dockerfile this case same directory.
      args:
        - DEV=true
    ports:   # To reach a container from the host, the ports must be exposed declaratively through the ports keyword
      - "8000:8000"
    volumes:
      - ./app:/app
    command: > # commands executed in the container on docker-compose up
      sh -c "python manage.py wait_for_db &&
             python manage.py migrate &&
             python manage.py runserver 0.0.0.0:8000"
    environment:
      - DB_HOST=db
      - DB_NAME=devdb
      - DB_USER=devuser
      - DB_PASSWORD=changeme
    depends_on:  # this service will wait for the -db to start first.
      - db

  db:
    image: postgres:13-alpine
    volumes:
      - dev-db-data:/var/lib/postgresql/data
    environment:    # default configuration for development.
      - POSTGRES_DB=devdb
      - POSTGRES_USER=devuser
      - POSTGRES_PASSWORD=changeme

volumes:
  dev-db-data:

```

Reference

docker-compose explained [blog](https://www.baeldung.com/ops/docker-compose)

Build: context: [build](https://docs.docker.com/compose/compose-file/compose-file-v3/#build)