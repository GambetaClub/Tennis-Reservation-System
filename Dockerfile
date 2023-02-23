FROM python:3.9-alpine3.13
LABEL maintainer="marigyt.maj@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./tokeneke /tokeneke

WORKDIR /tokeneke
EXPOSE 8001

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R tokeneke:tokeneke /vol && \
    chmod -R 755 /vol

ENV PATH="/py/bin:$PATH"

USER app