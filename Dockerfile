FROM python:3.9-alpine3.13
LABEL maintainer="selina"

ENV PYTHONBUFFERED 1

# These folders will be copied to the docker image
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
# our working directory is where our commands will be execured.
WORKDIR  /app
# connection between the container to our machine. 
EXPOSE 8000

ARG DEV=false

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

# update environment path for docker
ENV PATH="/py/bin:$PATH"

# this will switch our docker user from root to django user

USER django-user