#!/usr/bin/env python3
import os
import time
import json
import threading
import tinytuya
import paho.mqtt.client as mqtt
from dps_metadata import DPS_METADATA

# Umgebungsvariablen laden
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

# Verbindungsaufbau-Callback
def on_connect(client, userdata, flags, rc):
    print(f"✅ MQTT verbunden (Code {rc})")
    client.subscribe(f"{MQTT_COMMAND_TOPIC}/#")

# Nachricht empfangen
def on_message(client, userdata, msg):
    try:
        dps_key = msg.topic.split("/")[-1]
        meta = DPS_METADATA.get(dps_key, {})
        if not meta.get("writable"):
            print(f"⛔️ DPS {dps_key} ist nicht beschreibbar")
            return
        value = json.loads(msg.payload.decode())
        print(f"➡️ Befehl für DPS {dps_key}: {value}")
        device.set_value(dps_key, value)
    except Exception as e:
        print(f"❌ Fehler bei Nachricht: {e}")

client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT, 60)

# Discovery-Payload veröffentlichen
discovered = set()
def publish_discovery(dps_key):
    if dps_key in discovered:
        return
    discovered.add(dps_key)

    meta = DPS_METADATA.get(dps_key, {})
    name = meta.get("name", f"DPS {dps_key}")
    writable = meta.get("writable", False)
    dtype = meta.get("type", "str")

    base_id = f"dbs2300_{dps_key}"
    state_topic = f"{MQTT_TOPIC}/{dps_key}"
    cmd_topic = f"{MQTT_COMMAND_TOPIC}/{dps_key}"

    device_config = {
        "identifiers": ["dabbsson_dbs2300"],
        "name": "Dabbsson DBS2300",
        "model": "DBS2300",
        "manufacturer": "Dabbsson"
    }

    payload = {
        "name": name,
        "unique_id": base_id,
        "state_topic": state_topic,
        "device": device_config
    }

    component = "sensor"
    if writable:
        if dtype == "bool":
            component = "switch"
            payload.update({
                "command_topic": cmd_topic,
                "payload_on": "true",
                "payload_off": "false"
            })
        elif dtype == "int":
            component = "number"
            payload.update({
                "command_topic": cmd_topic,
                "min": 0,
                "max": 1000,
                "step": 1
            })
        elif dtype == "str":
            component = "text"
            payload["command_topic"] = cmd_topic

    # Zusatzinformationen für Home Assistant
    if dtype == "int" and not writable:
        if dps_key == "10":
            payload.update({"unit_of_measurement": "°C", "device_class": "temperature"})
        elif dps_key in ["1", "123", "138"]:
            payload.update({"unit_of_measurement": "%", "device_class": "battery"})
        elif dps_key in ["105", "108"]:
            payload.update({"unit_of_measurement": "W", "device_class": "power"})
        elif dps_key == "145":
            payload.update({"unit_of_measurement": "V", "device_class": "voltage"})

    discovery_topic = f"{MQTT_DISCOVERY_PREFIX}/{component}/dabbsson/{base_id}/config"
    print(f"🛰️ Discovery: {discovery_topic}")
    client.publish(discovery_topic, json.dumps(payload), retain=True)

# Status regelmäßig publizieren
def publish_loop():
    while True:
        try:
            dps = device.status().get("dps", {})
            for key, value in dps.items():
                if key in DPS_METADATA:
                    val_str = "true" if value is True else "false" if value is False else str(value)
                    topic = f"{MQTT_TOPIC}/{key}"
                    print(f"📤 DPS {key}: {val_str}")
                    client.publish(topic, val_str, retain=True)
                    publish_discovery(key)
        except Exception as e:
            print(f"⚠️ Fehler bei Statusabruf: {e}")
        time.sleep(5)

threading.Thread(target=publish_loop, daemon=True).start()
client.loop_forever()