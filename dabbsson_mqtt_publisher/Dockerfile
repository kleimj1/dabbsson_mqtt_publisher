# Dockerfile
ARG BUILD_FROM=ghcr.io/hassio-addons/base-python:10.0.0
FROM ${BUILD_FROM}

# Install Python dependencies
RUN pip install --no-cache-dir tinytuya paho-mqtt

# Copy Add-on files
COPY run.sh /run.sh
COPY mqtt_publisher.py /mqtt_publisher.py
RUN chmod a+x /run.sh

# Start
CMD ["/run.sh"]
