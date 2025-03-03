import pygame
from misc.settings import *

class Menu:
    def __init__(self, title, options, screen, font):
        self.title = title
        self.options = options
        self.selected_option = 0
        self.screen = screen
        self.font = font
        self.background = pygame.image.load('Graphics/Misc/menubackground-main.jpg')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.selected_option > 0:
                self.selected_option -= 1
            elif event.key == pygame.K_DOWN and self.selected_option < len(self.options) - 1:
                self.selected_option += 1

    def render(self):
        self.screen.blit(self.background, (0, 0))
        title_text = self.font.render(self.title, True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH / 2, HEIGHT / 4))
        self.screen.blit(title_text, title_rect)
        
        for i, option in enumerate(self.options):
            color = WHITE if i != self.selected_option else (255, 255, 0)
            option_text = self.font.render(option, True, color)
            option_rect = option_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + i * 40))
            self.screen.blit(option_text, option_rect)

        pygame.display.flip()