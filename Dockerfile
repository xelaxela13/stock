FROM python:3.8-alpine3.11
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /tmp/
RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
       gcc \
       libc-dev \
       libffi-dev \
       openssl-dev \
       gettext \
    && apk add --no-cache \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
       gdal \
       jpeg-dev \
       zlib-dev \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && apk del .build-deps \
    && rm -rf /tmp/requirements.txt \
    && rm -rf /var/cache/apk/*

RUN mkdir -p /home/stock
ENV PROJECT_ROOT /home/stock
ENV PATH $PATH:$PROJECT_ROOT
ENV PYTHONPATH $PYTHONPATH:$PROJECT_ROOT
WORKDIR $PROJECT_ROOT
COPY . $PROJECT_ROOT

#docker build -t xelaxela13/stock:latest .