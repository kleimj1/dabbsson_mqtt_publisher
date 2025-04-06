# Nutzt Python-Image von Home Assistant mit Pip
FROM ghcr.io/home-assistant/{arch}-base-python:3.11

# Installiere benötigte Python-Pakete
RUN pip3 install --no-cache-dir tinytuya paho-mqtt

# Kopiere das Skript und das Start-Skript
COPY run.sh /run.sh
COPY mqtt_publisher.py /mqtt_publisher.py
COPY dps_metadata.py /dps_metadata.py

# Mach das Startskript ausführbar
RUN chmod a+x /run.sh

# Führe das Add-on aus
CMD ["/run.sh"]
