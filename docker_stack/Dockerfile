FROM python:3.6.5

MAINTAINER Edwin Carrasquillo ecarra7979@gmail.com

# set work directory
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copying over application files ##
COPY recipes_app /usr/src/app
COPY rockitchef_project /usr/src/app
COPY staticfiles /usr/src/app
COPY manage.py /usr/src/app
COPY startup.sh /usr/src/app
COPY requirements.txt /usr/src/app

# Installing dependancies
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Running startup script to start django app
# & create admin user
ENTRYPOINT ["/usr/src/app/startup.sh"]
