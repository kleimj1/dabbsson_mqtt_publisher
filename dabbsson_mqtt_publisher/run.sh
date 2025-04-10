#!/bin/sh

mkdir -p /config/scripts
echo "📄 Erzeuge Dabbsson Discovery-Skript in Home Assistant scripts/"
cp /default_scripts/mqtt_discovery_refresh.yaml /config/scripts/ || echo "⚠️ Konnte Script nicht kopieren!"

/venv/bin/python /mqtt_publisher.py
