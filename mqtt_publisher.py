import os
import time
import json
import tinytuya
import threading
import paho.mqtt.client as mqtt
from dps_metadata import DPS_METADATA

DEVICE_ID = os.getenv("DEVICE_ID")
LOCAL_KEY = os.getenv("LOCAL_KEY")
IP = os.getenv("IP")
MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
MQTT_COMMAND_TOPIC = os.getenv("MQTT_COMMAND_TOPIC")
MQTT_DISCOVERY_PREFIX = os.getenv("MQTT_DISCOVERY_PREFIX", "homeassistant")

print("🚀 Starte Dabbsson MQTT Publisher mit Metadaten...")

device = tinytuya.OutletDevice(DEVICE_ID, IP, LOCAL_KEY)
device.set_version(3.4)
client = mqtt.Client()

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

    if writable and dtype == "bool":
        config_topic = f"{MQTT_DISCOVERY_PREFIX}/switch/dabbsson/{dps_key}/config"
        payload = {
            "name": name,
            "unique_id": unique_id,
            "state_topic": state_topic,
            "command_topic": f"{MQTT_COMMAND_TOPIC}/{dps_key}",
            "payload_on": "true",
            "payload_off": "false",
            "device": device_config,
            "icon": "mdi:toggle-switch"
        }
    else:
        config_topic = f"{MQTT_DISCOVERY_PREFIX}/sensor/dabbsson/{dps_key}/config"
        payload = {
            "name": name,
            "unique_id": unique_id,
            "state_topic": state_topic,
            "device": device_config,
            "icon": "mdi:chart-box-outline"
        }
        if dtype == "int":
            if dps_key == "10":
                payload.update({"unit_of_measurement": "°C", "device_class": "temperature"})
            elif dps_key in ["1", "123", "138"]:
                payload.update({"unit_of_measurement": "%", "device_class": "battery"})
            elif dps_key in ["105", "108"]:
                payload.update({"unit_of_measurement": "W", "device_class": "power"})
            elif dps_key == "145":
                payload.update({"unit_of_measurement": "V", "device_class": "voltage"})

    client.publish(config_topic, json.dumps(payload), retain=True)

def on_connect(client, userdata, flags, rc):
    print(f"✅ MQTT verbunden (Code {rc})")
    client.subscribe(f"{MQTT_COMMAND_TOPIC}/#")

def on_message(client, userdata, msg):
    try:
        dps_key = msg.topic.split("/")[-1]
        meta = DPS_METADATA.get(dps_key, {})
        if not meta.get("writable"):
            print(f"⛔️ DPS {dps_key} ist nicht beschreibbar")
            return
        raw = msg.payload.decode()
        value = json.loads(raw)
        device.set_dps({dps_key: value})
        print(f"➡️ Befehl für DPS {dps_key}: {value}")
    except Exception as e:
        print(f"❌ Fehler beim Schreiben an DPS {dps_key}: {e}")

client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT, 60)

def publish_loop():
    while True:
        try:
            status = device.status()
            dps = status.get("dps", {})
            for key, value in dps.items():
                if key not in DPS_METADATA:
                    continue
                client.publish(f"{MQTT_TOPIC}/{key}", str(value), retain=True)
                publish_discovery(key, value)
            time.sleep(5)
        except Exception as e:
            print(f"⚠️ Fehler beim Abrufen: {e}")
            time.sleep(10)

threading.Thread(target=publish_loop, daemon=True).start()
client.loop_forever()
