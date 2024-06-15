from typing import Dict
import shutil
import pathlib
import os
import json

# General path
PROGRAM_PATH: str = pathlib.Path(__file__).parent.resolve()
ASSET_PATH: str = os.path.join(PROGRAM_PATH, "assets")
APP_DATA: str = os.path.expanduser(os.path.join("~", ".hack"))
LOG_PATH: str = os.path.expanduser(os.path.join(APP_DATA, "log"))  # file


# Hackthebox specific constants
HTB_PATH: str = os.path.expanduser(os.path.join(APP_DATA, "htb"))
CACHE_PATH: str = os.path.expanduser(os.path.join(HTB_PATH, "cache.json"))  # file
HTB_OVPN: str = os.path.join(HTB_PATH, "vpn.ovpn")
HTB_SERVICE: str = (
    open(os.path.join(ASSET_PATH, "hackthebox.service")).read() % HTB_OVPN
)
HTP_POLKIT_ASSET: str = os.path.join(ASSET_PATH, "rules")
HTP_SERVICE_ASSET: str = os.path.join(ASSET_PATH, "hackthebox.service")
HTB_POLKIT_PATH: str = f"/etc/polkit-1/rules.d/haxtools-hackthebox.rules"
HTB_SERVICE_PATH: str = f"/etc/systemd/system/hackthebox.service"
REGIONS: Dict[int, Dict[str, str]] = {
    1: {"name": "EU Free 1"},
    201: {"name": "EU Free 2"},
    253: {"name": "EU Free 3"},
    113: {"name": "US Free 1"},
    202: {"name": "US Free 2"},
    254: {"name": "US Free 3"},
    177: {"name": "AU Free 1"},
    251: {"name": "SG Free 1"},
}


# Configuration content
CONFIG_PATH: str = os.path.join(APP_DATA, "config.json")
CONFIGURATION = None

try:
    json.load(open(CONFIG_PATH))
except FileNotFoundError:
    if not os.path.isfile(CONFIG_PATH):
        shutil.copyfile(os.path.join(ASSET_PATH, "config.json"), CONFIG_PATH)
finally:
    CONFIGURATION = json.load(open(CONFIG_PATH))
