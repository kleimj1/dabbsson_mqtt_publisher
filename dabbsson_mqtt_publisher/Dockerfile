ARG BUILD_FROM
FROM $BUILD_FROM

# Installiere Python-Pakete
RUN pip3 install --no-cache-dir tinytuya paho-mqtt

COPY run.sh /run.sh
COPY mqtt_publisher.py /mqtt_publisher.py
COPY dps_metadata.py /dps_metadata.py

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
