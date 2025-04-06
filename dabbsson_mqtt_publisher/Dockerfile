ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Installiere Python3 und pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Installiere Python-Abhängigkeiten
RUN pip3 install --no-cache-dir tinytuya paho-mqtt

# Dateien kopieren
COPY run.sh /run.sh
COPY mqtt_publisher.py /mqtt_publisher.py
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
