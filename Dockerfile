FROM python:3.8-alpine3.11
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /tmp/
RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
       gcc \
       postgresql-dev \
       musl-dev \
       gettext \
       postgresql-client \
    && apk add --no-cache \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
       gdal \
       jpeg-dev \
       zlib-dev \
       nodejs \
       nodejs-npm \
       libpq \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && apk del .build-deps \
    && rm -rf /tmp/requirements.txt \
    && rm -rf /var/cache/apk/*

# create directory for the app user
RUN mkdir -p /home/user
# create the app user
#RUN addgroup -S user && adduser -S user -G user

ENV PROJECT_ROOT /home/user/stock
ENV PATH $PATH:$PROJECT_ROOT
ENV PYTHONPATH $PYTHONPATH:$PROJECT_ROOT
RUN mkdir $PROJECT_ROOT
WORKDIR $PROJECT_ROOT

RUN npm -g install --save-dev @babel/core @babel/cli @babel/preset-env
RUN npm -g install yuglify sass

COPY . $PROJECT_ROOT

#RUN chown -R user:user $PROJECT_ROOT

#USER user

#docker build -t stock:latest .
#docker tag stock:latest xelaxela13/stock:latest