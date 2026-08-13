import json

def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except:
        return {"border": True, "clicks": True, "dark_theme": True, "hotkey": "F6"}

def save_settings(data):
    with open("settings.json", "w") as f:
        json.dump(data, f, indent=4)