FROM python:3.6-alpine
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1
ENV PROJECT_ROOT /home/stock
ENV PATH $PATH:$PROJECT_ROOT
ENV PYTHONPATH $PYTHONPATH:$PROJECT_ROOT
COPY . $PROJECT_ROOT
WORKDIR $PROJECT_ROOT
# common dependencies
RUN apk add --update\
    build-base \
    libpq \
    postgresql \
    postgresql-dev \
    # pillow dependencies
    jpeg-dev \
    zlib-dev \
    # i18n
    gettext \
    # node
    nodejs \
    nodejs-npm \
    mc \
    && rm -rf /var/cache/apk/*
RUN npm -g install --save-dev @babel/core @babel/cli @babel/preset-env
RUN npm -g install yuglify uglify-js sass
RUN pip3.6 install --upgrade pip
RUN pip3.6 install -r requirements.txt

#docker build -t stock:latest .
#docker tag stock:latest xelaxela13/stock:latest