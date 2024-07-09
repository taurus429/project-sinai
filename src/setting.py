import json
import os

SETTINGS_FILE = "settings.json"


class Setting:

    def __init__(self):
        self.settings = None
        self.load_settings()

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as file:
                self.settings = json.load(file)
        else:
            self.settings = dict()

    def set_settings(self, key, data):
        self.settings[key] = data
        self.save_settings(self.settings)

    def get_settings(self):
        return self.settings

    def save_settings(self, settings):
        with open(SETTINGS_FILE, 'w') as file:
            json.dump(settings, file, indent=4)