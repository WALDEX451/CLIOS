# bootstrap.py
import json
import uuid
import getpass
import platform
from pathlib import Path
from kernel import Kernel

CONFIG_FILE = Path("config.json")


def build_default_config():
    return {
        "password": "",
        "hostname": platform.node() or "raspberrypi",
        "username": getpass.getuser() or "pi",
        "user_id": str(uuid.uuid4()),
        "first_run": True,
        "profile": "raspberry-pi",
        "guardian_mode": True,
        "require_https": True,
        "verify_tls": True,
        "enforce_ssh_host_keys": True,
    }


def load_or_create_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    config = build_default_config()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
    print("[BOOTSTRAP] Nieuwe standaardconfig aangemaakt in config.json")
    return config

def load_version():
    return Path("version").read_text(encoding="utf-8").strip()

def boot():
    config = load_or_create_config()
    version = load_version()
    print(f"[BOOTSTRAP] CLIOS v{version} starten…")
    return Kernel(config=config, version=version)
