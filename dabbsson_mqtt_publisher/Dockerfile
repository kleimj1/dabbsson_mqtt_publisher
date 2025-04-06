ARG BUILD_FROM
FROM $BUILD_FROM

# Installiere grundlegende Abhängigkeiten und pip
RUN apk add --no-cache \
    python3 \
    py3-pip \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev

# Installiere Python-Pakete
RUN pip3 install --no-cache-dir tinytuya paho-mqtt

# Kopiere Skripte ins Image
COPY run.sh /run.sh
COPY mqtt_publisher.py /mqtt_publisher.py
COPY dps_metadata.py /dps_metadata.py

# Mach das Skript ausführbar
RUN chmod a+x /run.sh

# Starte das Skript
CMD [ "/run.sh" ]
