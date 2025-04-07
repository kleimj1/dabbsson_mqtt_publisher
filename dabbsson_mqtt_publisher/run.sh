#!/bin/bash

# Lade Konfiguration aus /data/options.json in Umgebungsvariablen
export DEVICE_ID=$(jq -r .device_id /data/options.json)
export LOCAL_KEY=$(jq -r .local_key /data/options.json)
export IP=$(jq -r .device_ip /data/options.json)
export MQTT_HOST=$(jq -r .mqtt_host /data/options.json)
export MQTT_PORT=$(jq -r .mqtt_port /data/options.json)
export MQTT_TOPIC=$(jq -r .mqtt_topic /data/options.json)
export MQTT_COMMAND_TOPIC=$(jq -r .mqtt_command_topic /data/options.json)
export MQTT_DISCOVERY_PREFIX=$(jq -r .mqtt_discovery_prefix /data/options.json)
export MQTT_USER=$(jq -r .mqtt_user /data/options.json)
export MQTT_PASSWORD=$(jq -r .mqtt_password /data/options.json)

echo "📦 Starte Dabbsson MQTT Publisher mit venv..."

# VENV anlegen, falls noch nicht vorhanden
if [ ! -d "/opt/venv" ]; then
  echo "📦 Erstelle Python venv..."
  python3 -m venv /opt/venv
  /opt/venv/bin/pip install --no-cache-dir tinytuya paho-mqtt
fi

# venv aktivieren und Skript starten
source /opt/venv/bin/activate
python3 /mqtt_publisher.py
