ARG BUILD_FROM
FROM $BUILD_FROM

# Installiere Python 3 und pip
RUN apk add --no-cache \
    python3 \
    py3-pip \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev && \
    python3 -m ensurepip && \
    pip3 install --no-cache-dir --upgrade pip

# Installiere Python-Abhängigkeiten
RUN pip3 install --no-cache-dir tinytuya paho-mqtt

# Kopiere Python-Dateien
COPY mqtt_publisher.py /mqtt_publisher.py
COPY dps_metadata.py /dps_metadata.py

COPY run.sh /run.sh
RUN chmod a+x /run.sh
CMD [ "/run.sh" ]

