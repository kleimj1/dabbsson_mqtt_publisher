ARG BUILD_FROM
FROM $BUILD_FROM

# Systempakete installieren (ohne bashio!)
RUN apk add --no-cache \
    python3 \
    py3-pip \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    jq

# Virtuelle Umgebung anlegen und aktivieren
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Python-Abhängigkeiten installieren
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir tinytuya paho-mqtt

# Skripte und Metadaten kopieren
COPY mqtt_publisher.py /mqtt_publisher.py
COPY dps_metadata.py /dps_metadata.py
COPY run.sh /run.sh

# Skript ausführbar machen
RUN chmod a+x /run.sh

# Startkommando
CMD [ "/run.sh" ]
