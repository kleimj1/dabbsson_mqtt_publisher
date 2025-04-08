# 🚀 Dabbsson MQTT Publisher – Home Assistant Add-on

Dieses Add-on liest über das Tuya-Protokoll (lokal via WLAN) **DPS-Werte von Dabbsson-Geräten wie DBS2300 & DBS600M** aus und veröffentlicht diese regelmäßig via **MQTT Discovery** an Home Assistant.

Damit werden **automatisch Sensoren & Schalter erstellt** – komplett lokal, ohne Tuya-Cloud oder Bluetooth!

---

## ✅ Funktionen

- 📡 Liest alle bekannten DPS-Werte (auch versteckte)
- 🔄 MQTT Discovery: automatische Sensor-/Schalter-Erstellung
- 🔧 Unterstützung für steuerbare Entitäten (z. B. AC Out, 12V, Ladeleistung)
- 🧠 Robuste Wiederverbindung & Logging
- ⚙️ Mehrgeräte-Support: DBS2300, DBS600M (frei kombinierbar)
- 🖥 UI-basierte Konfiguration via Home Assistant Add-on Panel

---

## 📦 Installation in Home Assistant

1. Öffne Home Assistant → **Einstellungen → Add-ons → Add-on Store**
2. Klicke oben rechts auf **„Add-on Repository hinzufügen“**
3. Füge dieses Repository ein:

```
https://github.com/kleimj1/dabbsson_mqtt_publisher
```

Oder direkt:

[![Add-on installieren](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https://github.com/kleimj1/dabbsson_mqtt_publisher)

4. Danach: `Dabbsson MQTT Publisher` installieren & konfigurieren

---

## ⚙️ Konfiguration (UI)

### 🔧 Geräte-Liste (Mehrere Geräte möglich!)

| Feld         | Beschreibung                                          |
|--------------|-------------------------------------------------------|
| `enabled`    | Gerät aktivieren (Checkbox)                           |
| `name`       | Anzeigename (wird im MQTT-Topic verwendet)            |
| `type`       | Gerätetyp: `dbs2300` oder `dbs600m`                    |
| `device_id`  | Tuya Device ID                                        |
| `local_key`  | Tuya Local Key                                        |
| `device_ip`  | Lokale IP-Adresse des Geräts                          |

### 🌐 MQTT-Verbindung

| Feld                   | Beschreibung                              |
|------------------------|--------------------------------------------|
| `mqtt_host`            | MQTT Broker Hostname (z. B. `core-mosquitto`) |
| `mqtt_port`            | Meist `1883`                               |
| `mqtt_user` / `password` | Zugangsdaten (optional)                   |
| `mqtt_discovery_prefix`| Normalerweise `homeassistant`             |

---

## 📡 MQTT Topics & Home Assistant Discovery

Dieses Add-on erzeugt automatisch MQTT Topics im Format:

```
dabbsson/<name>/dps/<dps_id>
```

### 🔍 Beispiel bei Gerät `DBS2300`:

| MQTT Topic                      | Beschreibung             | Schreibbar |
|---------------------------------|--------------------------|------------|
| `dabbsson/dbs2300/dps/1`        | SoC Batterie [%]         | ❌         |
| `dabbsson/dbs2300/dps/10`       | Temperatur [°C]          | ❌         |
| `dabbsson/dbs2300/dps/109`      | AC Out AN                | ✅         |
| `dabbsson/dbs2300/dps/123`      | Zielwert in Watt         | ✅         |
| `dabbsson/dbs600m/dps/108`      | Wechselrichter AN        | ✅         |

---

## ✉️ Steuerung per MQTT

```bash
mosquitto_pub -h localhost -t dabbsson/dbs2300/dps/109/set -m true
```

---

## 🔍 Device ID & Local Key finden

1. Erstelle ein Entwickler-Konto auf [https://iot.tuya.com](https://iot.tuya.com)
2. Erstelle ein Projekt und verknüpfe dein Smart Life Konto
3. Geräte importieren → Device-ID & Local-Key einsehen

👉 Alternativ über Tools wie `tuya-cli` oder `tuya-cloudcutter`

---

## 👀 Typische Entitäten in Home Assistant

Nach dem Start erscheinen automatisch z. B.:

- `sensor.dabbsson_soc_batterie_1`
- `sensor.dabbsson_temperatur`
- `switch.dabbsson_ac_out_an`
- `number.dabbsson_ladeleistung`

---

## 🧠 Hinweise

- Das Add-on läuft dauerhaft und pollt die Geräte alle 5 Sekunden
- Es verwendet nur lokale Verbindungen (kein Cloud-Zwang)
- MQTT-Topics sind kompatibel mit Home Assistant Discovery
- Alle DPS-Metadaten findest du in `dps_metadata/dbs2300.py` oder `dbs600m.py`
- Du kannst beliebig viele Geräte hinzufügen und kombinieren

---

## ❤️ Mitmachen

Fehlt dir ein DPS-Wert? Du willst ein anderes Gerät integrieren?

➡️ Erstelle ein GitHub Issue oder einen Pull Request:

👉 https://github.com/kleimj1/dabbsson_mqtt_publisher

---

## ✨ Viel Spaß mit deinem Dabbsson in Home Assistant!
