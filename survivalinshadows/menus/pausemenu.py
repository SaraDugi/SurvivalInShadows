import pygame
import sys
from .menu import Menu
from misc.settings import *

class PauseMenu(Menu):
    def __init__(self, title, options, level, screen, font, settings_manager, return_to_main, restart_level):
        if "Exit Game" not in options:
            options.append("Exit Game")
        if "Quit to Title" not in options:
            options.append("Quit to Title")
        if "Retry" not in options:
            options.append("Retry")

        super().__init__(title, options, screen, font)
        self.level = level
        self.settings_manager = settings_manager
        self.return_to_main = return_to_main
        self.restart_level = restart_level

        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h

        self.update_background()

    def update_background(self):
        global screen
        fullscreen_flag = pygame.FULLSCREEN if self.settings_manager.get_setting("fullscreen") else 0
        screen = pygame.display.set_mode((self.screen_width, self.screen_height), fullscreen_flag)
        self.screen = screen

        self.background = pygame.image.load('Graphics/Misc/menubackground-main.jpg')
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.selected_option > 0:
                self.selected_option -= 1
            elif event.key == pygame.K_DOWN and self.selected_option < len(self.options) - 1:
                self.selected_option += 1
            elif event.key == pygame.K_RETURN:
                chosen_option = self.options[self.selected_option]
                if chosen_option == "Resume":
                    return False
                elif chosen_option == "Settings":
                    from menus.settingsmenu import SettingsMenu
                    settings_menu = SettingsMenu(self.screen, self.font, self.settings_manager)
                    settings_menu.run()
                    self.update_background()
                elif chosen_option == "Quit to Title":
                    self.return_to_main()
                    return False
                elif chosen_option == "Retry":
                    self.restart_level()
                    return False
                elif chosen_option == "Exit Game":
                    pygame.quit()
                    sys.exit()
        return True

    def render(self):
        self.screen.blit(self.background, (0, 0))

        title_text = self.font.render(self.title, True, WHITE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        self.screen.blit(title_text, title_rect)

        for i, option in enumerate(self.options):
            color = WHITE if i != self.selected_option else RED
            text = self.font.render(option, True, color)

            text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + i * 50))  
            self.screen.blit(text, text_rect)

        pygame.display.flip()