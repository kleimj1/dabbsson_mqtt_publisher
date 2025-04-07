ARG BUILD_FROM
FROM $BUILD_FROM

# Installiere benötigte Pakete
RUN apk add --no-cache \
    python3 \
    py3-pip \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    bashio \
    jq

# Erstelle virtuelle Umgebung
RUN python3 -m venv /opt/venv

# Setze Pfad zur venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip und installiere Abhängigkeiten in venv
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir tinytuya paho-mqtt

# Kopiere Python-Dateien
COPY mqtt_publisher.py /mqtt_publisher.py
COPY dps_metadata.py /dps_metadata.py

# Kopiere Startskript
COPY run.sh /run.sh
RUN chmod a+x /run.sh

# Start
CMD [ "/run.sh" ]
