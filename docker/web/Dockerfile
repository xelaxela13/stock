FROM python:3.6
ENV PYTHONUNBUFFERED 1
ENV PROJECT_ROOT /srv/www/stock
COPY . $PROJECT_ROOT
WORKDIR $PROJECT_ROOT
#RUN python3 set_env_vars.py
RUN pip install --upgrade pip
RUN pip install pip-tools && pip-compile --output-file requirements.txt requirements.in
RUN pip install -r requirements.txt
RUN pip install flake8
RUN apt-get update && apt-get install -y gettext libgettextpo-dev