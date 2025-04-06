#!/bin/bash
export DEVICE_ID=$(jq -r .device_id /data/options.json)
export LOCAL_KEY=$(jq -r .local_key /data/options.json)
export IP=$(jq -r .ip /data/options.json)
export MQTT_HOST=$(jq -r .mqtt_host /data/options.json)
export MQTT_PORT=$(jq -r .mqtt_port /data/options.json)
export MQTT_TOPIC=$(jq -r .mqtt_topic /data/options.json)
export MQTT_COMMAND_TOPIC=$(jq -r .mqtt_command_topic /data/options.json)
export MQTT_DISCOVERY_PREFIX=$(jq -r .mqtt_discovery_prefix /data/options.json)
#!/usr/bin/with-contenv bashio

echo "🔧 Installiere Python-Abhängigkeiten..."
pip3 install --no-cache-dir tinytuya paho-mqtt

echo "🚀 Starte MQTT Publisher..."

/usr/bin/python3 /mqtt_publisher.py
