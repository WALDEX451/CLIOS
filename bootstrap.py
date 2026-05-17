# bootstrap.py
import json
import uuid
import getpass
from pathlib import Path
from kernel import Kernel

CONFIG_FILE = Path("config.json")

def load_or_create_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    # eerste keer opstarten
    password = getpass.getpass("Create your password: ")
    hostname = input("Your computer hostname: ")
    username = input("Your username: ")
    user_id  = str(uuid.uuid4())

    config = {
        "password": password,
        "hostname": hostname,
        "username": username,
        "user_id": user_id,
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
    return config

def load_version():
    return Path("version").read_text(encoding="utf-8").strip()

def boot():
    config = load_or_create_config()
    version = load_version()
    print(f"[BOOTSTRAP] CLIOS v{version} starten…")
    return Kernel(config=config, version=version)