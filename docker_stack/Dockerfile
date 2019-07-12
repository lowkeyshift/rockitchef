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


COPY . /usr/src/app
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/startup.sh"]
