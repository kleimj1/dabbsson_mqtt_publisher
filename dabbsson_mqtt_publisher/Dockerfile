ARG BUILD_FROM
FROM $BUILD_FROM

# Systemabhängigkeiten installieren
RUN apk add --no-cache \
    python3 \
    py3-pip \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev

# Erstelle ein virtuelles Python-Environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV VENV_PATH=/data/venv
RUN python3 -m venv $VENV_PATH

# Installiere Abhängigkeiten im venv
RUN $VENV_PATH/bin/pip install --no-cache-dir --upgrade pip && \
    $VENV_PATH/bin/pip install --no-cache-dir tinytuya paho-mqtt

# Kopiere Skripte
COPY mqtt_publisher.py /mqtt_publisher.py
COPY dps_metadata.py /dps_metadata.py
COPY run.sh /run.sh

# Rechte setzen
RUN chmod +x /run.sh

# Starte das Script
CMD ["/run.sh"]
