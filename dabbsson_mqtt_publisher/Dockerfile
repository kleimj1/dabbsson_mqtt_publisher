ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Python-Abhängigkeiten
RUN pip install --no-cache-dir tinytuya paho-mqtt

# Skripte und Startdatei kopieren
COPY run.sh /run.sh
COPY mqtt_publisher.py /mqtt_publisher.py
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
