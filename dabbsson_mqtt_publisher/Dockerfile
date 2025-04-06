ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# System-Pakete und Python installieren
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev gcc libc-dev

# Python-Abhängigkeiten installieren
RUN pip3 install --no-cache-dir tinytuya paho-mqtt

# Skripte und Startdatei kopieren
COPY run.sh /run.sh
COPY mqtt_publisher.py /mqtt_publisher.py
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
