#!/usr/bin/env python3
import os
import time
import json
import threading
import tinytuya
import paho.mqtt.client as mqtt
from dps_metadata import DPS_METADATA

# Konfiguration aus Umgebungsvariablen
DEVICE_ID = os.getenv("DEVICE_ID")
LOCAL_KEY = os.getenv("LOCAL_KEY")
DEVICE_IP = os.getenv("DEVICE_IP")
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "dabbsson/status")
MQTT_COMMAND_TOPIC = os.getenv("MQTT_COMMAND_TOPIC", "dabbsson/command")
MQTT_DISCOVERY_PREFIX = os.getenv("MQTT_DISCOVERY_PREFIX", "homeassistant")
MQTT_USER = os.getenv("MQTT_USER", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")

print("🚀 Starte Dabbsson MQTT Publisher...")

# Tuya-Gerät initialisieren
try:
    device = tinytuya.OutletDevice(DEVICE_ID, DEVICE_IP, LOCAL_KEY)
    device.set_version(3.4)
except Exception as e:
    print(f"❌ Fehler beim Initialisieren des Geräts: {e}")
    exit(1)

# MQTT-Client vorbereiten
client = mqtt.Client()
if MQTT_USER:
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

# MQTT → Discovery Payloads senden
def publish_discovery(dps_key, value):
    meta = DPS_METADATA.get(dps_key, {})
    name = meta.get("name", f"DPS {dps_key}")
    writable = meta.get("writable", False)
    dtype = meta.get("type", "str")
    unique_id = f"dabbsson_{dps_key}"
    state_topic = f"{MQTT_TOPIC}/{dps_key}"

    device_config = {
        "identifiers": ["dabbsson_dbs2300"],
        "name": "Dabbsson DBS2300",
        "model": "DBS2300",
        "manufacturer": "Dabbsson"
    }

    if writable:
        if dtype == "bool":
            component = "switch"
            payload = {
                "state_topic": state_topic,
                "command_topic": f"{MQTT_COMMAND_TOPIC}/{dps_key}",
                "payload_on": "true",
                "payload_off": "false",
                "icon": "mdi:toggle-switch"
            }
        elif dtype == "int":
            component = "number"
            payload = {
                "state_topic": state_topic,
                "command_topic": f"{MQTT_COMMAND_TOPIC}/{dps_key}",
                "min": 0,
                "max": 1000,
                "step": 1,
                "icon": "mdi:counter"
            }
        elif dtype == "str":
            component = "text"
            payload = {
                "state_topic": state_topic,
                "command_topic": f"{MQTT_COMMAND_TOPIC}/{dps_key}",
                "icon": "mdi:text"
            }
        else:
            component = "sensor"
            payload = {
                "state_topic": state_topic,
                "icon": "mdi:chart-box-outline"
            }
    else:
        component = "sensor"
        payload = {
            "state_topic": state_topic,
            "icon": "mdi:chart-box-outline"
        }

    if dtype == "int" and not writable:
        if dps_key == "10":
            payload.update({"unit_of_measurement": "°C", "device_class": "temperature"})
        elif dps_key in ["1", "123", "138"]:
            payload.update({"unit_of_measurement": "%", "device_class": "battery"})
        elif dps_key in ["105", "108"]:
            payload.update({"unit_of_measurement": "W", "device_class": "power"})
        elif dps_key == "145":
            payload.update({"unit_of_measurement": "V", "device_class": "voltage"})

    payload.update({
        "name": name,
        "unique_id": unique_id,
        "device": device_config
    })

    topic = f"{MQTT_DISCOVERY_PREFIX}/{component}/dabbsson/{dps_key}/config"
    client.publish(topic, json.dumps(payload), retain=True)

# Callback bei MQTT-Connect
def on_connect(client, userdata, flags, rc):
    print(f"✅ MQTT verbunden (Code {rc})")
    client.subscribe(f"{MQTT_COMMAND_TOPIC}/#")

# Callback bei MQTT-Nachricht
def on_message(client, userdata, msg):
    try:
        dps_key = msg.topic.split("/")[-1]
        meta = DPS_METADATA.get(dps_key, {})
        if not meta.get("writable"):
            print(f"⛔️ DPS {dps_key} ist nicht beschreibbar")
            return
        raw = msg.payload.decode()
        value = json.loads(raw)
        print(f"➡️ Befehl für DPS {dps_key}: {value}")
        device.set_dps({dps_key: value})
    except Exception as e:
        print(f"❌ Fehler beim Verarbeiten von {msg.topic}: {e}")

client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT, 60)

# Daten-Publishing-Schleife
def publish_loop():
    while True:
        try:
            status = device.status()
            dps = status.get("dps", {})
            for key, value in dps.items():
                if key in DPS_METADATA:
                    client.publish(f"{MQTT_TOPIC}/{key}", str(value), retain=True)
                    publish_discovery(key, value)
            time.sleep(5)
        except Exception as e:
            print(f"⚠️ Fehler beim Abrufen der Daten: {e}")
            time.sleep(10)

threading.Thread(target=publish_loop, daemon=True).start()
client.loop_forever()
