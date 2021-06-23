FROM python:3.8-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /tmp/
RUN apt-get update \
    && apt-get install gcc libffi-dev libpq-dev openssl -y \
    && apt-get clean \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm -rf /tmp/requirements.txt
ENV PROJECT_ROOT /home/stock
ENV PATH $PATH:$PROJECT_ROOT
ENV PYTHONPATH $PYTHONPATH:$PROJECT_ROOT
RUN mkdir -p $PROJECT_ROOT
WORKDIR $PROJECT_ROOT
COPY . $PROJECT_ROOT

#docker build -t xelaxela13/stock:latest .