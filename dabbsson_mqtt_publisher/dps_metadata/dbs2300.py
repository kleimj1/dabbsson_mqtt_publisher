DPS_METADATA = {
    # === Allgemein / Batterie ===
    "1":   {"name": "Batterie SoC",              "type": "int",  "unit": "%",    "writable": False},
    "2":   {"name": "Verbleibende Zeit",         "type": "int",  "unit": "min",  "writable": False},
    "10":  {"name": "Temperatur",                "type": "int",  "unit": "°C",   "writable": False},

    # === AC/USB/DC Steuerung ===
    "25":  {"name": "Beep (Tonsignal)",          "type": "bool", "writable": True},
    "109": {"name": "AC Ausgang EIN/AUS",        "type": "bool", "writable": True},
    "111": {"name": "DC 12V EIN/AUS",            "type": "bool", "writable": True},
    "112": {"name": "USB 5V EIN/AUS",            "type": "bool", "writable": True},

    # === Anzeige- & LED-Zustände ===
    "102": {"name": "LED-Status",                "type": "enum", "options": ["off", "dim", "bright", "sos"], "writable": True},
    "127": {"name": "Systemmodus",               "type": "enum", "options": ["standby_mode", "eco_mode"],     "writable": False},
    "128": {"name": "Smart Charging EIN/AUS",    "type": "bool", "writable": True},

    # === Leistungsmessung ===
    "103": {"name": "PV Eingang",                "type": "int",  "unit": "W",    "writable": False},
    "104": {"name": "AC Eingang",                "type": "int",  "unit": "W",    "writable": False},
    "105": {"name": "Batterie1 Out",             "type": "int",  "unit": "W",    "writable": False},
    "106": {"name": "Batterie2 Out",             "type": "int",  "unit": "W",    "writable": False},
    "107": {"name": "Ausgang Gesamt",            "type": "int",  "unit": "W",    "writable": False},
    "108": {"name": "AC Ausgang Leistung",       "type": "int",  "unit": "W",    "writable": False},
    "110": {"name": "12V Ausgang",               "type": "int",  "unit": "W",    "writable": False},
    "113": {"name": "USBA1 Leistung",            "type": "int",  "unit": "W",    "writable": False},
    "114": {"name": "USBA2 Leistung",            "type": "int",  "unit": "W",    "writable": False},
    "115": {"name": "USBA3 Leistung",            "type": "int",  "unit": "W",    "writable": False},
    "116": {"name": "USBC1 Leistung",            "type": "int",  "unit": "W",    "writable": False},
    "117": {"name": "USBC2 Leistung",            "type": "int",  "unit": "W",    "writable": False},
    "118": {"name": "USBC3 Leistung",            "type": "int",  "unit": "W",    "writable": False},
    "131": {"name": "Eingang Gesamtleistung",    "type": "int",  "unit": "W",    "writable": False},

    # === Lademodi & Leistung ===
    "123": {"name": "AC Ziel-Ladeleistung",      "type": "int",  "unit": "W",    "writable": True},
    "124": {"name": "Fast/Slow Charge Hinweis",  "type": "bool", "writable": False},

    # === Zeitsteuerung ===
    "120": {"name": "AC Einschaltzeit",          "type": "enum", "options": ["30_minutes", "1_hour", "2_hours", "6_hours", "12_hours", "close_timing"], "writable": True},
    "121": {"name": "LCD Aus-Zeit",              "type": "enum", "options": ["10_seconds", "30_seconds", "1_minute", "5_minutes", "30_minutes", "close_timing"], "writable": True},
    "122": {"name": "AC Auto-Ausschaltzeit",     "type": "enum", "options": ["2_hours", "4_hours", "6_hours", "12_hours", "24_hours", "close_timing"], "writable": True},

    # === Geräteinformationen ===
    "130": {"name": "PD Firmware",               "type": "str",  "writable": False},
    "132": {"name": "BMS Firmware",              "type": "str",  "writable": False},
    "133": {"name": "Inverter Firmware",         "type": "str",  "writable": False},
    "140": {"name": "Seriennummer",              "type": "str",  "writable": False},
    "143": {"name": "OTA Update-Zeit",           "type": "int",  "unit": "s",    "writable": False},

    # === Steuerfunktionen ===
    "129": {"name": "Gerät ausschalten",         "type": "bool", "writable": True},
    "142": {"name": "Werksreset",                "type": "bool", "writable": True},
    "144": {"name": "App-Heartbeat",             "type": "bool", "writable": True},
    "145": {"name": "Netzspannung einstellen",   "type": "int",  "unit": "V",    "writable": True},

    # === Fehlerstatus (lesbar, optional Mapping) ===
    "134": {"name": "Inverter Fehler",           "type": "int",  "writable": False},
    "136": {"name": "BMS Fehler",                "type": "int",  "writable": False},
    "137": {"name": "BMS Fehler 1",              "type": "int",  "writable": False}
}
