#!/usr/bin/with-contenv bashio

export DEVICE_ID=$(bashio::config 'device_id')
export LOCAL_KEY=$(bashio::config 'local_key')
export IP=$(bashio::config 'ip')
export MQTT_HOST=$(bashio::config 'mqtt_host')
export MQTT_PORT=$(bashio::config 'mqtt_port')
export MQTT_TOPIC=$(bashio::config 'mqtt_topic')
export MQTT_COMMAND_TOPIC=$(bashio::config 'mqtt_command_topic')
export MQTT_DISCOVERY_PREFIX=$(bashio::config 'mqtt_discovery_prefix')

python3 /mqtt_publisher.py
