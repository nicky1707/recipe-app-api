# recipe-app-api
Recipe api project.

## Dockerfile breakdown
```sh

RUN python -m env /py && \
    /py/bin/pip install --upgrade pip && \ #
    /py/bin/pip install -r /tmp/requirements.ext && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

```

line 1 : create a virtual env

line 2 : upgrade pip

line 3 : install dependencies in requirements.txt

line 4 : removes the requirements.txt file

line 5 : adding a new user inside our docker image because we dont want to use the root user

_because if application gets compromised the attacker gets the full access_

line 6 : No password will set and require for the user.

line 7 : Dont create a home directory for the user.

line 8 : user name.


## docker-compose.yml Breakdown

```docker

version: "3.9"

services:
  app:
    build:
      context: .
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app
    command: >
      sh -c "python manage.py runserver 0.0.0.0:8000"

```

line 1 : Verion of the docker compose syntax

line 2 : services of docker container typically docker can have one or more services.

line 3 : **app:** service name

line 4 : build command build it in context directory

line 5 : **context : .** refers the current directory commad runs.

line 6 : ports map our host machine port 8000 to docker images port 8000

line 7 : volumes way of mapping our directories from our system to docker image.

line 8 : command: is the command use to run the service

