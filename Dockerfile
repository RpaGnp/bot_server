# Imagen base más ligera con soporte para Python
FROM python:3.10-alpine

# Evitar el almacenamiento en búfer en la salida de Python
ENV PYTHONUNBUFFERED=1
# Agregar el directorio de scripts al PATH
ENV PATH="/scripts:${PATH}"

# Configuración de zona horaria
RUN cp /usr/share/zoneinfo/America/Bogota /etc/localtime

# Instalar dependencias del sistema
RUN apk add --update --no-cache \
    bash \
    libxslt \
    openblas \
    libstdc++ \
    dos2unix \
    mariadb-connector-c-dev \
    gcc \
    g++ \
    linux-headers \
    libc-dev \
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
    python3-dev \
    libjpeg-turbo-dev \
    zlib-dev \
    freetype-dev \
    libpng-dev \
    openblas-dev \
    gfortran

# Instalar pip y dependencias del proyecto
COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /requirements.txt

# Eliminar dependencias de compilación para reducir el tamaño de la imagen
RUN apk del g++ gcc linux-headers libc-dev libxml2-dev libxslt-dev libffi-dev python3-dev

# Crear el directorio de la aplicación y configurarlo como el directorio de trabajo
RUN mkdir /app
WORKDIR /app

# Copiar la aplicación y scripts al contenedor
COPY ./app /app
COPY ./scripts /scripts

# Hacer ejecutables los scripts y convertirlos a formato Unix
RUN chmod +x /scripts/* && dos2unix /scripts/*

# Comando predeterminado para ejecutar el contenedor
CMD ["bash", "/scripts/script.sh"]
