DPS_METADATA = {
    "101": {"name": "PV-Leistung",        "type": "int",  "unit": "W",  "writable": False},
    "103": {"name": "PV-Spannung",        "type": "int",  "unit": "V",  "writable": False},
    "111": {"name": "PV-Strom",           "type": "int",  "unit": "A",  "writable": False},
    "104": {"name": "Inverter-Temp",      "type": "int",  "unit": "°C", "writable": False},
    "109": {"name": "AC Ausgang Leistung","type": "int",  "unit": "W",  "writable": False},
    "120": {"name": "Batterie SoC",       "type": "int",  "unit": "%",  "writable": False},
    "108": {"name": "Wechselrichter EIN/AUS", "type": "bool", "writable": True},
    "126": {"name": "Arbeitsmodus",       "type": "enum", "options": ["0", "1"], "writable": True},  # "eco" / "charge"
    "110": {"name": "Power Limit",        "type": "int",  "unit": "%",  "writable": True},
    "105": {"name": "Zähler zurücksetzen","type": "bool", "writable": True}
}
