import sys
import pygame
from settings import TILESIZE
from csvimport import import_csv_layout
from enemy import Enemy
from tiledmap import TiledMap
from tile import Tile
from player import Player
from ui import *

class Level:
    def __init__(self, mission_name):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.mission_name = mission_name
        self.create_map(mission_name)
        self.ui = UI()
        self.player = Player((2450, 800),[self.visible_sprites],self.obstacle_sprites)
        self.enemy = Enemy(mission_name,'1',(1850, 800), [self.visible_sprites],self.obstacle_sprites)
        self.enemies = [self.enemy] 

    def create_map(self,mission_name):
        layouts = {
            'boundary': import_csv_layout('Graphics/Map/CSV/abandonefactory_limit.csv'),
            'entities': import_csv_layout('Graphics/Map/CSV/abandonefactory_entities.csv'),
            'enemy': import_csv_layout('Graphics/Map/CSV/abandonefactory_enemy.csv')
        }
        
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        elif style == 'entities':
                            if col == '394':
                                self.player = Player((x, y),[self.visible_sprites],self.obstacle_sprites)
                        elif style == 'enemy':
                            if col == '0':
                                self.enemy = Enemy(mission_name,'1',(x, y), [self.visible_sprites], self.obstacle_sprites)

    def game_over_screen(self, display_surface):
        screen_width, screen_height = 800, 600

        display_surface.fill(BLACK)

        game_over_font = pygame.font.Font(None, 100)
        game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
        game_over_text_rect = game_over_text.get_rect(center=(screen_width / 2, screen_height / 4))
        display_surface.blit(game_over_text, game_over_text_rect)

        button_font = pygame.font.Font(None, 50)
        button_width, button_height = 300, 50

        restart_button = pygame.Rect(screen_width / 2 - button_width / 2, screen_height / 2, button_width, button_height)
        pygame.draw.rect(display_surface, (255, 255, 255), restart_button)  
        restart_text = button_font.render("Restart", True, (0, 0, 0))  
        restart_text_rect = restart_text.get_rect(center=restart_button.center)  
        display_surface.blit(restart_text, restart_text_rect) 

        quit_button = pygame.Rect(screen_width / 2 - button_width / 2, screen_height / 2 + button_height + 20, button_width, button_height)
        pygame.draw.rect(display_surface, (255, 255, 255), quit_button)  
        quit_text = button_font.render("Quit", True, (0, 0, 0))  
        quit_text_rect = quit_text.get_rect(center=quit_button.center) 
        display_surface.blit(quit_text, quit_text_rect) 

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_button.collidepoint(mouse_pos):
                        running = True
                        start_menu = True
                        mission_menu = False
                        selected_option = 0
                        break
                    elif quit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
            pygame.display.flip()

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.ui.display(self.player)

        for enemy in self.enemies:
            if pygame.sprite.collide_rect(self.player, enemy):
                self.game_over_screen(self.display_surface)
                return

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor = pygame.image.load("Graphics/Map/map/abandonefactory.png").convert()
        self.floor_rect = self.floor.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor, floor_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            if sprite == player:
                offset_pos = (self.half_width - player.rect.width // 2, self.half_height - player.rect.height // 2)
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
