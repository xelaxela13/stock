###########
# BUILDER #
###########

# pull official base image
FROM python:3.8.0-alpine as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add build-base postgresql-dev gcc python3-dev musl-dev py-setuptools \
    # pillow
    jpeg-dev \
    zlib-dev \
    # i18n
    gettext \
    # node
    nodejs \
    nodejs-npm

# lint
RUN pip install --upgrade pip
RUN pip install flake8
COPY . /usr/src/app/
RUN flake8 --ignore=E501,F401 .

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########

# pull official base image
FROM python:3.8.0-alpine

# create directory for the app user
RUN mkdir -p /home/user

# create the app user
RUN addgroup -S user && adduser -S user -G user

ENV PROJECT_ROOT /home/user/stock
ENV PATH $PATH:$PROJECT_ROOT
ENV PYTHONPATH $PYTHONPATH:$PROJECT_ROOT
RUN mkdir $PROJECT_ROOT
WORKDIR $PROJECT_ROOT

# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

## common dependencies
#RUN apk add --update \
#    build-base \
#    libpq \
#    postgresql \
#    postgresql-dev \
#    gcc \
#    python3-dev \
#    musl-dev \
#    # pillow dependencies
#    jpeg-dev \
#    zlib-dev \
#    # i18n
#    gettext \
#    # node
#    nodejs \
#    nodejs-npm \
#    && rm -rf /var/cache/apk/*
RUN npm -g install --save-dev @babel/core @babel/cli @babel/preset-env
RUN npm -g install yuglify sass
#RUN pip3.8 install --upgrade pip
#RUN pip3.8 install -r requirements.txt

COPY . $PROJECT_ROOT

# chown all the files to the app user
RUN chown -R user:user $PROJECT_ROOT

# change to the app user
USER user

#docker build -t stock:latest .
#docker tag stock:latest xelaxela13/stock:latest