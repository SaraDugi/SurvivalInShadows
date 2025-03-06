import pygame
from misc.settings import *
from .item import Item

class StaminaPotion(Item):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.item_path = "Graphics/Item_models/stamina"
        self.image = pygame.image.load(f"{self.item_path}/StaminaPotion.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hit_box = self.rect.inflate(0, 0)
        self.obstacle_sprites = obstacle_sprites

    def update(self, player):
        if self.rect.colliderect(player.rect):
            # Only pick up if player's stamina is not full.
            if player.stamina.stamina_counter < player.stamina.max_stamina:
                player.inventory.add_item(self)
                print("Stamina Potion picked up!")
                self.kill()
            else:
                print("Stamina is full. Potion cannot be picked up.")