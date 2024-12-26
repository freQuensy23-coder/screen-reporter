import os
import json
from pathlib import Path

CONFIG_DIR = os.path.expanduser("~/.config/activity_tracker")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

def load_config() -> dict:
    if not os.path.exists(CONFIG_FILE):
        return {}
    
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config: dict):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def get_credentials() -> tuple[int | None, str | None]:
    config = load_config()
    return config.get("user_id"), config.get("secret_key")

def save_credentials(user_id: int, secret_key: str):
    config = load_config()
    config["user_id"] = user_id
    config["secret_key"] = secret_key
    save_config(config)