FROM python:3.6
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1
ENV PROJECT_ROOT /srv/www/stock
COPY . $PROJECT_ROOT
WORKDIR $PROJECT_ROOT
RUN apt-get update && apt-get install -y curl gettext libgettextpo-dev
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash
RUN apt-get install nodejs
RUN npm -g install yuglify sass babel-cli babel-core babel-preset-env babel-plugin-transform-remove-strict-mode
#RUN python3 set_env_vars.py
RUN pip install pip-tools && pip-compile --output-file requirements.txt requirements.in
RUN pip install --upgrade -r requirements.txt
