import sys
import pygame
from misc.settings import *
from misc.settingsmanager import SettingsManager

class Menu:
    def __init__(self, title, options, screen, font):
        self.title = title
        self.options = options
        self.selected_option = 0
        self.screen = screen
        self.font = font
        self.settings_manager = SettingsManager()

        self.update_screen()

    def update_screen(self):
        global screen
        display_info = pygame.display.Info()
        self.actual_width = display_info.current_w
        self.actual_height = display_info.current_h

        fullscreen_flag = pygame.FULLSCREEN if self.settings_manager.get_setting("fullscreen") else 0
        screen = pygame.display.set_mode((self.actual_width, self.actual_height), fullscreen_flag)
        self.screen = screen

        self.background = pygame.image.load("Graphics/Misc/menubackground-main.jpg")
        self.background = pygame.transform.scale(self.background, (self.actual_width, self.actual_height))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.selected_option > 0:
                self.selected_option -= 1
            elif event.key == pygame.K_DOWN and self.selected_option < len(self.options) - 1:
                self.selected_option += 1
            elif event.key == pygame.K_RETURN:
                chosen_option = self.options[self.selected_option]
                if chosen_option == "Toggle Fullscreen":
                    self.settings_manager.toggle_fullscreen()
                    self.update_screen()
                elif chosen_option == "Quit Game":
                    pygame.quit()
                    sys.exit()

    def render(self):
        self.screen.blit(self.background, (0, 0))

        title_text = self.font.render(self.title, True, WHITE)
        title_rect = title_text.get_rect(center=(self.actual_width / 2, self.actual_height / 4))
        self.screen.blit(title_text, title_rect)

        for i, option in enumerate(self.options):
            color = WHITE if i != self.selected_option else (255, 255, 0)
            option_text = self.font.render(option, True, color)
            option_rect = option_text.get_rect(center=(self.actual_width / 2, self.actual_height / 2 + i * 50))
            self.screen.blit(option_text, option_rect)

        pygame.display.flip()