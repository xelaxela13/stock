FROM python:3.8.0-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /tmp/
RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
        --repository http://dl-cdn.alpinelinux.org/alpine/v3.9/main \
       gcc \
       postgresql-dev \
       musl-dev \
    && apk add --no-cache \
        --repository http://dl-cdn.alpinelinux.org/alpine/v3.9/main \
       gettext \
       postgresql-client \
    && apk add --no-cache \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
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