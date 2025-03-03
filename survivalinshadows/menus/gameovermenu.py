import pygame
import sys
from misc.settings import BLACK, WHITE, DARK_RED, GAMEOVER_OPTIONS

class GameOverScreen:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.screen_width, self.screen_height = display_surface.get_size()
        self.button_font = pygame.font.Font(None, 50)
        self.message_font = pygame.font.Font(None, 100)
        self.button_width, self.button_height = 300, 50

    def render(self):
        self.display_surface.fill(BLACK)

        message_surface = self.message_font.render("Game Over", True, DARK_RED)
        message_rect = message_surface.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
        self.display_surface.blit(message_surface, message_rect)

        buttons = []
        for i, option in enumerate(GAMEOVER_OPTIONS):
            button = pygame.Rect(
                self.screen_width / 2 - self.button_width / 2, 
                self.screen_height / 2 + 150 + i * (self.button_height + 20), 
                self.button_width, self.button_height
            )
            pygame.draw.rect(self.display_surface, WHITE, button)
            text = self.button_font.render(option, True, BLACK)
            text_rect = text.get_rect(center=button.center)
            self.display_surface.blit(text, text_rect)
            buttons.append(button)

        pygame.display.flip()
        return buttons

    def handle_events(self, buttons):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, button in enumerate(buttons):
                        if button.collidepoint(mouse_pos):
                            if GAMEOVER_OPTIONS[i] == 'Quit Game':
                                pygame.quit()
                                sys.exit()
            pygame.display.flip()