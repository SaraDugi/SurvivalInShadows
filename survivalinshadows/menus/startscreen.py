import pygame
from misc.settings import WHITE
from .menu import Menu

pygame.init()

class StartScreen(Menu):
    def __init__(self, title, instructions, screen, font, settings_manager):
        self.settings_manager = settings_manager

        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h

        super().__init__(title, [], screen, font)

        self.instructions = instructions
        self.update_screen()

    def update_screen(self):
        global screen
        fullscreen_flag = pygame.FULLSCREEN if self.settings_manager.get_setting("fullscreen") else 0
        screen = pygame.display.set_mode((self.screen_width, self.screen_height), fullscreen_flag)
        self.screen = screen

        self.background = pygame.image.load("Graphics/Misc/menubackground-main.jpg")
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))

    def render(self):
        self.screen.blit(self.background, (0, 0))

        title_text = self.font.render(self.title, True, WHITE)
        title_rect = title_text.get_rect(center=(self.screen_width / 2, self.screen_height / 4))
        self.screen.blit(title_text, title_rect)
        
        for i, instruction in enumerate(self.instructions):
            text = self.font.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(self.screen_width / 2, self.screen_height / 2 + (i - len(self.instructions) / 2) * 60))
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            return False
        return True