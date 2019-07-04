FROM python:3.6.5

MAINTAINER Edwin Carrasquillo ecarra7979@gmail.com

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

ADD . /usr/src/app/
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python3 -m venv venv
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

#CMD ["./wait-for-postgres.sh"]
EXPOSE 8000
#CMD ["./startup.sh"]
