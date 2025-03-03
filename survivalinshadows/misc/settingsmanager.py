import json
import pygame
from misc.settings import *

SETTINGS_FILE = "settings.json"

class SettingsManager:
    def __init__(self):
        self.settings = {
            "volume": 0.5,
            "fullscreen": False
        }
        self.load_settings()

    def load_settings(self):
        """
        Loads settings from a JSON file.
        """
        try:
            with open(SETTINGS_FILE, "r") as file:
                self.settings.update(json.load(file))
        except FileNotFoundError:
            self.save_settings()

    def save_settings(self):
        """
        Saves settings and applies changes globally.
        """
        with open(SETTINGS_FILE, "w") as file:
            json.dump(self.settings, file, indent=4)

        # ✅ Apply fullscreen mode immediately
        self.apply_fullscreen()

    def get_setting(self, key):
        return self.settings.get(key, None)

    def adjust_volume(self, change):
        """
        Adjusts volume using a slider.
        """
        self.settings["volume"] = max(0.0, min(1.0, self.settings["volume"] + change))
        pygame.mixer.music.set_volume(self.settings["volume"])
        self.save_settings()

    def toggle_fullscreen(self):
        """
        Toggles fullscreen mode and applies it globally.
        """
        self.settings["fullscreen"] = not self.settings["fullscreen"]
        self.save_settings()

    def apply_fullscreen(self):
        """
        Updates the display mode based on the fullscreen setting.
        """
        global screen
        fullscreen_flag = pygame.FULLSCREEN if self.settings["fullscreen"] else 0
        screen = pygame.display.set_mode((WIDTH, HEIGHT), fullscreen_flag)
        pygame.display.flip()