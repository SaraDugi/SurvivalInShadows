import pygame
import sys
from .menu import Menu
from misc.settings import *

class PauseMenu(Menu):
    def __init__(self, title, options, mission_name, level, screen, font):
        super().__init__(title, options, screen, font)
        self.mission_name = mission_name
        self.level = level

    def handle_event(self, event, level):
        self.screen.fill(BLACK)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.selected_option > 0:
                self.selected_option -= 1
            elif event.key == pygame.K_DOWN and self.selected_option < len(self.options) - 1:
                self.selected_option += 1
            elif event.key == pygame.K_RETURN:
                chosen_option = self.options[self.selected_option]
                if chosen_option == 'Resume':
                    return False
                elif chosen_option == 'Quit Game':
                    pygame.quit()
                    sys.exit()

        return True

    def render(self):
        super().render()