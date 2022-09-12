FROM python:3.9-alpine3.13
LABEL maintainer="selina"

ENV PYTHONUNBUFFERED 1

# Copy folders from local drive to container image.
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

# working directory is where the docker run commands will be execured.
WORKDIR /app

# connection port between the container to our machine.
EXPOSE 8000

ARG DEV=false

# 1. apk is tha package manager for alpine linux.
# 2. --virtual create a new virtual package name '.tmp-build-deps'
#       with the listed dependencies (build-base, postgresql-dev, musl-dev).
# 3. rm -rf removes the requirements.txt file in the /tmp folder.
# 4. 'add user --disabled-password' creates a user 'django-user'
#        with no password, home dir.
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# update environment path. It specifies the directories to be searched to find a command.
ENV PATH="/py/bin:$PATH"

#switch our docker image user from root to django-user.
USER django-user