import pygame
from misc.settings import *
from levels.level import *

class Item(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.direction = pygame.math.Vector2()