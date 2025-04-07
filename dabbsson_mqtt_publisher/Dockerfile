ARG BUILD_FROM
FROM $BUILD_FROM

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apk add --no-cache python3 bashio py3-pip gcc musl-dev libffi-dev openssl-dev python3-dev && \
    python3 -m venv $VIRTUAL_ENV && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir tinytuya paho-mqtt

COPY mqtt_publisher.py /mqtt_publisher.py
COPY dps_metadata.py /dps_metadata.py
COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD [ "/run.sh" ]
