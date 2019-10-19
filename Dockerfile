FROM python:3.6.9-alpine3.10
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1
ENV PROJECT_ROOT /srv/www/stock
ENV PYTHONPATH $PYTHONPATH:$PROJECT_ROOT
COPY . $PROJECT_ROOT
WORKDIR $PROJECT_ROOT
# common dependencies
RUN apk add --update\
    alpine-sdk \
    py-setuptools \
    postgresql-dev \
    python3-dev \
    jpeg-dev \
    zlib-dev \
    gettext \
    nodejs \
    nodejs-npm \
    && rm -rf /var/cache/apk/*
RUN npm -g install --save-dev @babel/core @babel/cli @babel/preset-env
RUN npm -g install mc yuglify uglify-js sass
RUN pip install --upgrade pip
RUN pip install pip-tools && pip-compile --output-file requirements.txt requirements.in
RUN pip install -r requirements.txt
