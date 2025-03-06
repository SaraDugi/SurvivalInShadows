import pygame
from misc.settings import *
from misc.csvimport import import_csv_layout
from entities.enemy import Enemy
from misc.camera import YSortCameraGroup
from mechanisms.heartbeat import Heartbeat
from misc.tile import Tile
from entities.player import Player
from menus.gameovermenu import GameOverScreen
from mechanisms.torch import TorchEffect  
from items.staminapotion import StaminaPotion 
from items.healthpotion import HealthPotion

class Level:    
    def __init__(self, mission_name, settings_manager):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.mission_name = mission_name
        self.settings_manager = settings_manager
        self.create_map(mission_name)
        self.player = Player(PLAYER_START_POS, [self.visible_sprites], self.obstacle_sprites)
        self.enemy = Enemy(mission_name, '1', ENEMY_START_POS, [self.visible_sprites], self.obstacle_sprites)
        self.enemies = [self.enemy] 
        self.heartbeat = Heartbeat()
        self.torch_effect = TorchEffect()
        self.spawn_potions()

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

    def spawn_potions(self):
        potion_x = self.player.rect.x + TILESIZE * 2  
        potion_y = self.player.rect.y

        stamina_potion = StaminaPotion((potion_x, potion_y), [self.visible_sprites, self.item_sprites], self.obstacle_sprites)
        health_potion = HealthPotion((potion_x + TILESIZE, potion_y), [self.visible_sprites, self.item_sprites], self.obstacle_sprites)
        self.item_sprites.add(stamina_potion, health_potion)

    def run(self, is_torch_effect):
        self.visible_sprites.custom_draw(self.player, is_torch_effect)

        self.player.update()
        self.visible_sprites.enemy_update(self.player)

        for item in self.item_sprites:
            item.update(self.player)  

        self.heartbeat.update(self.player, self.enemy)
        self.heartbeat.draw(self.display_surface)

        font = pygame.font.SysFont(None, FONT_SIZE)
        self.player.draw_ui(self.display_surface, font)

        if is_torch_effect:
            self.torch_effect.draw_light_mask(self.display_surface, self.player)

        if self.player.health <= 0:
            self.show_game_over_screen()

    def show_game_over_screen(self):
        game_over = GameOverScreen(self.display_surface)
        buttons = game_over.render()
        game_over.handle_events(buttons)