#!/usr/bin/env python3
import json, time, threading
import tinytuya
import paho.mqtt.client as mqtt
from dps_metadata import get_dps_metadata

CONFIG_PATH = "/data/options.json"

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

devices = []
for dev in config.get("devices", []):
    if not dev.get("enabled"):
        continue
    try:
        d = tinytuya.OutletDevice(dev["device_id"], dev["device_ip"], dev["local_key"])
        d.set_version(3.4)
        dev["device"] = d
        dev["dps_metadata"] = get_dps_metadata(dev["type"])
        dev["suffix"] = dev.get("suffix", "").lower()
        devices.append(dev)
        print(f"✅ Gerät {dev['name']} ({dev['type']}) verbunden")
    except Exception as e:
        print(f"❌ Fehler beim Initialisieren von {dev['name']}: {e}")

MQTT_HOST = config.get("mqtt_host", "localhost")
MQTT_PORT = config.get("mqtt_port", 1883)
MQTT_PREFIX = config.get("mqtt_discovery_prefix", "homeassistant")
MQTT_USER = config.get("mqtt_user", "")
MQTT_PASSWORD = config.get("mqtt_password", "")

client = mqtt.Client()
if MQTT_USER:
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

def get_base_name(device):
    suffix = f"-{device['suffix']}" if device.get("suffix") else ""
    return f"dabbsson/{device['name'].lower()}{suffix}"

def publish_discovery(device, dps_key, meta):
    base = get_base_name(device)
    state_topic = f"{base}/dps/{dps_key}"
    cmd_topic = f"{base}/dps/{dps_key}/set"
    dtype = meta.get("type", "str")
    writable = meta.get("writable", False)

    payload = {
        "name": meta.get("name", f"DPS {dps_key}"),
        "unique_id": f"{base}_{dps_key}",
        "device": {
            "identifiers": [base],
            "name": device["name"],
            "model": device["type"].upper(),
            "manufacturer": "Dabbsson"
        },
        "state_topic": state_topic
    }

    if writable:
        if dtype == "bool":
            comp = "switch"
            payload.update({
                "command_topic": cmd_topic,
                "payload_on": "true",
                "payload_off": "false"
            })
        elif dtype == "int":
            comp = "number"
            payload.update({
                "command_topic": cmd_topic,
                "min": 0,
                "max": 1000,
                "step": 1
            })
        elif dtype == "enum":
            comp = "select"
            payload.update({
                "command_topic": cmd_topic,
                "options": meta.get("options", [])
            })
        else:
            comp = "text"
            payload["command_topic"] = cmd_topic
    else:
        comp = "sensor"

    topic = f"{MQTT_PREFIX}/{comp}/{base}_{dps_key}/config"
    client.publish(topic, json.dumps(payload), retain=True)

def on_message(client, userdata, msg):
    try:
        for dev in devices:
            base = get_base_name(dev) + "/dps/"
            if msg.topic.startswith(base):
                dps_key = msg.topic.split("/")[-2]
                meta = dev["dps_metadata"].get(dps_key)
                if not meta or not meta.get("writable"):
                    return
                value = json.loads(msg.payload.decode())
                if meta["type"] == "bool":
                    value = value in ["true", True, 1]
                print(f"➡️ Sende {value} an DPS {dps_key} ({dev['name']})")
                dev["device"].set_value(dps_key, value)
    except Exception as e:
        print(f"❌ Fehler bei MQTT-Befehl: {e}")

client.on_message = on_message

def publish_loop(device):
    base = get_base_name(device) + "/dps"
    while True:
        try:
            status = device["device"].status().get("dps", {})
            for key, val in status.items():
                meta = device["dps_metadata"].get(str(key))
                if not meta:
                    continue
                value = "true" if val is True else "false" if val is False else str(val)
                topic = f"{base}/{key}"
                client.publish(topic, value, retain=True)
                publish_discovery(device, str(key), meta)
        except Exception as e:
            print(f"⚠️ Fehler beim Abrufen von {device['name']}: {e}")
        time.sleep(5)

client.connect(MQTT_HOST, MQTT_PORT, 60)
client.subscribe("dabbsson/+/dps/+/set")
for dev in devices:
    threading.Thread(target=publish_loop, args=(dev,), daemon=True).start()
client.loop_forever()
