FROM ghcr.io/home-assistant/amd64-base-debian:latest

RUN apk add --no-cache python3 py3-pip
RUN pip3 install tinytuya paho-mqtt

COPY run.sh /run.sh
COPY mqtt_publisher.py /mqtt_publisher.py
RUN chmod a+x /run.sh

CMD ["/run.sh"]
