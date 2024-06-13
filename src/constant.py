import pathlib
import os
import json

# General path
PROGRAM_PATH: str = pathlib.Path(__file__).parent.resolve()
ASSET_PATH: str = os.path.join(PROGRAM_PATH, "assets")
APP_DATA: str = os.path.expanduser(os.path.join("~", ".hack"))
LOG_PATH: str = os.path.expanduser(os.path.join(APP_DATA, "log"))  # file


# Hackthebox specific paths
HTB_PATH: str = os.path.expanduser(os.path.join(APP_DATA, "htb"))
CACHE_PATH: str = os.path.expanduser(os.path.join(HTB_PATH, "cache.json"))  # file


# Configuration content
CONFIG_PATH: str = os.path.join(APP_DATA, "config.json")
CONFIGURATION = None
