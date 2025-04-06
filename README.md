# 🚀 Dabbsson MQTT Publisher – Home Assistant Add-on

Dieses Add-on liest über das Tuya-Protokoll (lokal via WLAN) **DPS-Werte vom Dabbsson DBS2300** aus und veröffentlicht diese regelmäßig via **MQTT Discovery** an Home Assistant.

Damit werden **automatisch Sensoren & Schalter** erstellt – komplett lokal, ohne Tuya-Cloud oder Bluetooth!

---

## ✅ Funktionen

- 📡 Liest alle bekannten DPS-Werte (auch versteckte)
- 🔄 MQTT Discovery: automatische Sensor-/Schalter-Erstellung
- 🔧 Unterstützung für steuerbare Entitäten (z. B. AC Out, 12V, Zielwert)
- 🧠 Robuste Wiederverbindung & Logging
- 🖥 UI-basierte Konfiguration

---

## 📦 Installation in Home Assistant

1. Öffne Home Assistant → **Einstellungen → Add-ons → Add-on Store**
2. Klicke oben rechts auf **„Add-on Repository hinzufügen“**
3. Füge dieses Repository ein:

https://github.com/kleimj1/dabbsson_mqtt_publisher


Oder klicke direkt hier:

[![Add-on installieren](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https://github.com/kleimj1/dabbsson_mqtt_publisher)

4. Danach: `Dabbsson MQTT Publisher` installieren & konfigurieren

---

## ⚙️ Konfiguration (UI)

| Feld                   | Beschreibung                                  |
|------------------------|----------------------------------------------|
| `device_id`            | Tuya Device ID deines DBS2300                |
| `local_key`            | Tuya Local Key                               |
| `ip`                   | Lokale IP-Adresse (z. B. `192.168.178.30`)    |
| `mqtt_host`            | MQTT Broker Hostname/IP (z. B. `core-mosquitto`) |
| `mqtt_port`            | Meist `1883`                                 |
| `mqtt_topic`           | z. B. `dabbsson`                              |
| `mqtt_discovery_prefix`| Meist `homeassistant`                        |

---

## 📡 MQTT Topics & Home Assistant Discovery

Dieses Add-on erzeugt automatisch MQTT Topics im Format:

### **Beispielhafte Topics:**

| MQTT Topic                  | Beschreibung               | Schreibbar |
|----------------------------|----------------------------|------------|
| `dabbsson/status/1`        | SoC Batterie [%]           | ❌         |
| `dabbsson/status/10`       | Temperatur [°C]            | ❌         |
| `dabbsson/status/109`      | AC Out AN                  | ✅         |
| `dabbsson/status/111`      | USB 5V AN                  | ✅         |
| `dabbsson/status/112`      | DC 12V AN                  | ✅         |
| `dabbsson/status/123`      | AC Zielwert %              | ✅         |
| `dabbsson/status/145`      | Netzspannung               | ✅         |

### Steuerung per MQTT:

``bash mosquitto_pub -h localhost -t dabbsson/command/109 -m true 


### 🔍 Device ID & Local Key finden
Erstelle ein Tuya Cloud Projekt: https://iot.tuya.com

Verknüpfe dein Smart Life Konto

Gerät → Device-ID & Local-Key einsehen

👉 Alternativ über Tools wie tuya-cli

---

### 👀 Typische Entitäten in Home Assistant
Nach der Installation erscheinen z. B.:

sensor.dabbsson_soc_batterie_1

sensor.dabbsson_temperatur

switch.dabbsson_ac_out_an

switch.dabbsson_usb_5v_an

---

### 🧠 Hinweise
Das Add-on läuft dauerhaft und liest alle 5 Sekunden

MQTT-Verbindung wird automatisch aufrechterhalten

Discovery erfolgt über den Prefix homeassistant

DPS-Definition & Metadaten in dps_metadata.py

---

### ❤️ Mitmachen
Fehlt dir ein DPS-Wert oder möchtest du helfen?

➡️ Erstelle ein GitHub Issue oder einen Pull Request unter:
https://github.com/kleimj1/dabbsson_mqtt_publisher

---

### 🧠 Viel Spaß mit deinem Dabbsson in Home Assistant!
yaml
Kopieren
Bearbeiten

---
