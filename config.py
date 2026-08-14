import json
import os
import sys

def get_settings_path():
    if sys.platform.startswith("win"):
        appdata_dir = os.environ.get("APPDATA", os.path.expanduser("~"))
    else:
        appdata_dir = os.path.expanduser("~/.config")

    app_folder = os.path.join(appdata_dir, "AutoClickerPro")
    os.makedirs(app_folder, exist_ok=True)
    
    return os.path.join(app_folder, "settings.json")

def load_settings():
    path = get_settings_path()
    if not os.path.exists(path):
        default_settings = {"border": True, "clicks": True, "dark_theme": True, "topmost": True, "safety_lock": True, "hotkey": "F6"}
        save_settings(default_settings)
        return default_settings

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_settings(settings_dict):
    path = get_settings_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(settings_dict, f, indent=4)