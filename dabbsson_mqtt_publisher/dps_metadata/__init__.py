from . import dbs2300, dbs600m

DPS_MAP = {
    "dbs2300": dbs2300.DPS_METADATA,
    "dbs600m": dbs600m.DPS_METADATA
}

def get_dps_metadata(device_type):
    """Gibt die Metadaten für den Gerätetyp zurück."""
    return DPS_MAP.get(device_type, {})
