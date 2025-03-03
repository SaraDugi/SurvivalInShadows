import pygame
from settings import *

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor = pygame.image.load("Graphics/Map/map/abandonefactory.png").convert()
        self.floor_rect = self.floor.get_rect(topleft=(0, 0))
        self.night = pygame.Surface((WIDTH, HEIGHT))
        self.torch_mask = pygame.image.load(TORCH_EFFECT_IMAGE).convert_alpha()
        self.torch_mask = pygame.transform.scale(self.torch_mask, TORCH_RADIUS)
        self.torch_mask_rect = self.torch_mask.get_rect()

    def custom_draw(self, player, is_torch_effect):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor, floor_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            if sprite == player:
                offset_pos = (self.half_width - player.rect.width // 2, self.half_height - player.rect.height // 2)
            self.display_surface.blit(sprite.image, offset_pos)
        
        if is_torch_effect:
            self.night.fill(NIGHT_COLOR)
            self.torch_mask_rect.center = player.rect.center
            offset_pos = (self.half_width - self.torch_mask_rect.width // 2, self.half_height - self.torch_mask_rect.height // 2)
            self.night.blit(self.torch_mask, offset_pos)
            self.display_surface.blit(self.night, (0, 0), special_flags=pygame.BLEND_MULT)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)