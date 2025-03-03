import sys
import pygame
import json
from misc.settings import *
from misc.settingsmanager import SettingsManager  # ✅ Import settings manager

class SettingsMenu:
    def __init__(self, screen, font, settings_manager):
        """
        Handles the settings menu with fullscreen toggle and volume slider.
        """
        self.screen = screen
        self.font = font
        self.settings_manager = settings_manager
        self.selected_option = 0

        # ✅ Adjust width & height dynamically
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h

        # ✅ Volume slider settings
        self.slider_x = self.screen_width // 2 + 120  
        self.slider_y = self.screen_height // 2 - 10
        self.slider_width = 200
        self.slider_height = 10

        # ✅ Load current settings temporarily
        self.temp_settings = self.settings_manager.settings.copy()

        # ✅ Update fullscreen label dynamically
        self.update_options()

    def update_options(self):
        """
        Updates the options list based on fullscreen state.
        """
        fullscreen_status = "ON" if self.temp_settings["fullscreen"] else "OFF"
        self.options = [f"Fullscreen: {fullscreen_status}", "Volume", "Save Settings", "Cancel"]

    def handle_event(self, event):
        """
        Handles menu navigation, volume adjustments, and fullscreen toggle.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.selected_option > 0:
                self.selected_option -= 1
            elif event.key == pygame.K_DOWN and self.selected_option < len(self.options) - 1:
                self.selected_option += 1
            elif event.key == pygame.K_LEFT and self.selected_option == 1:
                self.temp_settings["volume"] = max(0.0, self.temp_settings["volume"] - 0.05)
            elif event.key == pygame.K_RIGHT and self.selected_option == 1:
                self.temp_settings["volume"] = min(1.0, self.temp_settings["volume"] + 0.05)
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:  # ✅ Toggle Fullscreen
                    self.toggle_fullscreen()
                elif self.selected_option == 2:  # ✅ Save Settings
                    self.save_settings()
                    return False
                elif self.selected_option == 3:  # ✅ Cancel without saving
                    return False

    def toggle_fullscreen(self):
        """
        Toggles fullscreen mode and updates screen dynamically.
        """
        self.temp_settings["fullscreen"] = not self.temp_settings["fullscreen"]
        self.apply_fullscreen(self.temp_settings["fullscreen"])
        self.update_options()  # ✅ Update text dynamically

    def apply_fullscreen(self, enable):
        """
        Applies fullscreen setting instantly.
        """
        global screen
        mode = pygame.FULLSCREEN if enable else 0
        screen = pygame.display.set_mode((self.screen_width, self.screen_height), mode)
        self.screen = screen

    def save_settings(self):
        """
        Saves settings permanently and applies fullscreen.
        """
        self.settings_manager.settings = self.temp_settings.copy()
        self.settings_manager.save_settings()
        self.apply_fullscreen(self.settings_manager.get_setting("fullscreen"))

    def render(self):
        """
        Renders the settings menu with proper scaling.
        """
        self.screen.fill(BLACK)

        title = self.font.render("Settings", True, WHITE)
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, self.screen_height // 4))

        for i, option in enumerate(self.options):
            color = WHITE if i != self.selected_option else RED
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(self.screen_width // 2 - 100, self.screen_height // 2 + i * 50))
            self.screen.blit(text, text_rect)

            if i == 1:  # ✅ Draw volume slider next to "Volume"
                volume = self.temp_settings["volume"]
                slider_fill = int(self.slider_width * volume)
                pygame.draw.rect(self.screen, WHITE, (self.slider_x, text_rect.y + 5, self.slider_width, self.slider_height))
                pygame.draw.rect(self.screen, GREEN, (self.slider_x, text_rect.y + 5, slider_fill, self.slider_height))

        pygame.display.flip()

    def run(self):
        """
        Runs the settings menu loop.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.selected_option in [2, 3]:
                    running = False
                else:
                    result = self.handle_event(event)
                    if result is False:
                        return
            self.render()