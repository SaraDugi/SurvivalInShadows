import pygame
from misc.settings import *

class TorchEffect:
    def __init__(self):
        self.transparency = 0
        self.light_radius = 100

    def draw_light_mask(self, screen, player):
        fog = pygame.Surface((screen.get_width(), screen.get_height()))
        fog.fill((0, 0, 0))
        fog.set_alpha(self.transparency) 

        player_x, player_y = player.rect.center

        pygame.draw.circle(fog, (0, 0, 0, 0), (player_x, player_y), self.light_radius)
        screen.blit(fog, (0, 0))