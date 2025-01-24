FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1
ENV PATH="/scripts:${PATH}"

RUN cp /usr/share/zoneinfo/America/Bogota /etc/localtime

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache libxslt openblas libstdc++ dos2unix mariadb-connector-c-dev
# Instalar paquetes necesarios
RUN apk add --update --no-cache \
    gcc g++ linux-headers libc-dev libxml2-dev libxslt-dev libffi-dev python3-dev \
    libjpeg-turbo-dev zlib-dev freetype-dev libpng-dev openblas-dev gfortran \
    dos2unix mariadb-connector-c-dev

# Instalar pip y dependencias Python
RUN pip install --upgrade pip \
    && pip install -r /requirements.txt

# Limpiar dependencias temporales
RUN apk del g++ gcc linux-headers libc-dev libxml2-dev libxslt-dev libffi-dev python3-dev


RUN apk update && apk add bash

RUN mkdir /app
WORKDIR /app
COPY ./app /app
COPY ./scripts /scripts

RUN chmod +x /scripts/* && dos2unix /scripts/* 

CMD [ "script.sh" ]
# CMD [ "entrypoint.sh" ]
