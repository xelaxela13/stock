FROM alpine:3.10
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1
ENV PROJECT_ROOT /srv/www/stock
ENV PYTHONPATH $PYTHONPATH:$PROJECT_ROOT
COPY . $PROJECT_ROOT
WORKDIR $PROJECT_ROOT
RUN apk add --no-cache gettext nodejs npm
RUN npm install --save-dev @babel/core @babel/cli @babel/preset-env
RUN npm install mc yuglify uglify-js sass
RUN pip install --upgrade pip
RUN pip install pip-tools && pip-compile --output-file requirements.txt requirements.in
RUN pip install -r requirements.txt
