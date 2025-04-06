# 🚀 Dabbsson MQTT Publisher – Home Assistant Add-on

Dieses Add-on liest über das Tuya-Protokoll (lokal via WLAN) **DPS-Werte vom Dabbsson DBS2300** und veröffentlicht diese regelmäßig via **MQTT Discovery** in Home Assistant.

Damit werden **automatisch Sensoren & Schalter** erzeugt – vollständig lokal, ohne Tuya Cloud oder Bluetooth!

---

## ✅ Features

- 📡 Liest alle bekannten DPS-Werte (auch versteckte)
- 🔁 Veröffentlicht alle Daten automatisch über MQTT Discovery
- 🔧 Unterstützung für beschreibbare Schalter (AC Out, 5V, 12V etc.)
- 🖥 Konfigurierbar über Add-on UI
- 🧠 Automatische Wiederverbindung & Logging

---

## 📦 Installation in Home Assistant

1. Navigiere in Home Assistant zu **Einstellungen → Add-ons → Add-on Store**
2. Klicke rechts oben auf **„Add-on Repository hinzufügen“**
3. Füge folgendes Repository hinzu:

https://github.com/kleimj1/dabbsson_mqtt_publisher


Oder klick direkt hier:

[![Add-on installieren](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https://github.com/kleimj1/dabbsson_dbs2300)

4. Wähle **`Dabbsson MQTT Publisher`** aus der Liste und installiere das Add-on
5. Starte das Add-on nach Eingabe der Konfiguration

---

## ⚙️ Konfiguration (UI-basiert)

| Feld                   | Beschreibung                                  |
|------------------------|----------------------------------------------|
| `device_id`            | Tuya Device ID deines DBS2300                |
| `local_key`            | Tuya Local Key                               |
| `ip`                   | Lokale IP-Adresse (z. B. `192.168.178.30`)    |
| `mqtt_host`            | MQTT Broker (z. B. `core-mosquitto`)         |
| `mqtt_port`            | Meist `1883`                                 |
| `mqtt_topic`           | z. B. `dabbsson`                              |
| `mqtt_discovery_prefix`| Meist `homeassistant`                        |

---

## 📡 MQTT Beispiel-Topics (automatisch erstellt)

| Topic                          | Beschreibung             | Schreibbar |
|--------------------------------|--------------------------|------------|
| `dabbsson/status/1`           | SoC Batterie [%]         | ❌         |
| `dabbsson/status/10`          | Temperatur [°C]          | ❌         |
| `dabbsson/status/109`         | AC Out AN                | ✅         |
| `dabbsson/status/111`         | USB 5V AN                | ✅         |
| `dabbsson/status/112`         | DC 12V AN                | ✅         |
| `dabbsson/status/123`         | Zielwert AC-Ladung [%]   | ✅         |
| `dabbsson/status/145`         | Netzspannung             | ✅         |

Werte setzen mit z. B.:

```bash
mosquitto_pub -h localhost -t dabbsson/command/109 -m true

🔐 So bekommst du device_id und local_key
Registriere dich bei https://iot.tuya.com

Erstelle ein Cloud-Projekt und verknüpfe dein Smart Life Konto

Gerät hinzufügen → Device-ID & Local-Key kopieren

👀 Beispielhafte Entitäten in HA
Nach dem Start erscheinen automatisch z. B.:

sensor.dabbsson_temperatur

sensor.dabbsson_soc_batterie_1

switch.dabbsson_ac_out_an

switch.dabbsson_usb_5v_an

🧠 Nützliches
Add-on läuft dauerhaft und sendet Daten alle 5 Sekunden

Schreibbare Entitäten lassen sich über MQTT steuern

MQTT Discovery erfolgt vollständig automatisch

Logging erfolgt in Echtzeit im Add-on Protokoll

❤️ Mitmachen
Fehlt dir ein Sensor oder möchtest du helfen?
➡️ Erstelle ein GitHub Issue oder Pull Request!

🧠 Viel Spaß mit deinem Dabbsson in Home Assistant!
