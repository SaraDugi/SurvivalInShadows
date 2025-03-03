import math
import sys
import pygame
from settings import *
from csvimport import import_csv_layout
from enemy import Enemy
from camera import YSortCameraGroup
from heartbeat import Heartbeat
from tile import Tile
from player import Player

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_RED = (139, 0, 0)  
GHOST_WHITE = (248, 248, 255)  

class Level:    
    def __init__(self, mission_name):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.mission_name = mission_name
        self.create_map(mission_name)
        self.player = Player(PLAYER_START_POS, [self.visible_sprites], self.obstacle_sprites)
        self.enemy = Enemy(mission_name, '1', ENEMY_START_POS, [self.visible_sprites], self.obstacle_sprites)
        self.enemies = [self.enemy] 
        self.heartbeat = Heartbeat()

    def create_map(self, mission_name):
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
                                self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)
                        elif style == 'enemy':
                            if col == '0':
                                None

    def draw_light_mask(self, screen):
        fog = pygame.Surface((screen.get_width(), screen.get_height()))  
        fog.fill((0, 0, 0)) 
        transparency = 128  
        fog.set_alpha(transparency)  
        light_radius = 100  
        pygame.draw.circle(fog, (0, 0, 0, 0), self.rect.center, light_radius) 
        screen.blit(fog, (0, 0))  

    def game_over_screen(self, display_surface):
        screen_width, screen_height = display_surface.get_size()
        display_surface.fill(BLACK)
        button_font = pygame.font.Font(None, 50)
        button_width, button_height = 300, 50
        
        message_text = "Game Over"
        message_color = DARK_RED
        message_font = pygame.font.Font(None, 100)  
        message_surface = message_font.render(message_text, True, message_color)
        message_rect = message_surface.get_rect(center=(screen_width / 2, screen_height / 2))

        display_surface.blit(message_surface, message_rect)

        buttons = []
        for i, option in enumerate(GAMEOVER_OPTIONS):
            button = pygame.Rect(screen_width / 2 - button_width / 2, screen_height / 2 + 150 + i * (button_height + 20), button_width, button_height)
            pygame.draw.rect(display_surface, (255, 255, 255), button)
            text = button_font.render(option, True, (0, 0, 0))
            text_rect = text.get_rect(center=button.center)
            display_surface.blit(text, text_rect)
            buttons.append(button)

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

    def run(self, is_torch_effect):
        self.visible_sprites.custom_draw(self.player, is_torch_effect)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.heartbeat.update(self.player, self.enemy)
        self.heartbeat.draw(self.display_surface)
        
        for enemy in self.enemies:
            if pygame.sprite.collide_rect(self.player, enemy):
                self.game_over_screen(self.display_surface)
                return