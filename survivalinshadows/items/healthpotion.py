import pygame
from misc.settings import *
from misc.csvimport import import_folder
from .item import Item

class HealthPotion(Item):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.item_path = "Graphics/Item_models/health"
        self.image = pygame.image.load(f"{self.item_path}/HealthPotion.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hit_box = self.rect.inflate(0, 0)
        self.obstacle_sprites = obstacle_sprites

    def update(self, player):
        if self.rect.colliderect(player.rect):
            # Check if the player's health is full.
            if player.health == player.stats['health']:
                print("Health is already full. Potion not used.")
            else:
                # Heal the player to full health.
                player.health = player.stats['health']
                print("Health fully restored!")
                self.kill()