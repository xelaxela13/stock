FROM python:3.6
ENV PYTHONUNBUFFERED 1
COPY . /srv/www/stock
WORKDIR /srv/www/stock
RUN pip install --upgrade pip
RUN pip install pip-tools && pip-compile --output-file requirements.txt requirements.in
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y gettext libgettextpo-dev
RUN python3 set_env_vars.py