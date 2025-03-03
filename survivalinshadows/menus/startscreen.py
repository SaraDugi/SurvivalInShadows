import pygame
from misc.settings import WIDTH, HEIGHT, FONT_SIZE, WHITE
from .menu import Menu

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Survival in Shadows')
pygame.font.init() 
pygame.mixer.init()
font = pygame.font.SysFont(None, FONT_SIZE)

background = pygame.image.load('Graphics/Misc/menubackground-main.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

class StartScreen(Menu):
    def __init__(self, title, instructions, screen, font):
        super().__init__(title, [], screen, font)
        self.instructions = instructions

    def render(self):
        screen.blit(background, (0, 0))
        title_text = font.render(self.title, True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH / 2, HEIGHT / 4))
        screen.blit(title_text, title_rect)
        
        for i, instruction in enumerate(self.instructions):
            text = font.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + (i - len(self.instructions) / 2) * 60))
            screen.blit(text, text_rect)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            return False
        return True