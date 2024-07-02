import datetime
import math
import sys
from tkinter import font
import pygame
from settings import *
from csvimport import import_csv_layout
from enemy import Enemy
from game_stats import GameStats
from camera import YSortCameraGroup
from heartbeat import Heartbeat
from tile import Tile
from player import Player

class Level:
    def __init__(self, mission_name):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.mission_name = mission_name
        self.create_map(mission_name)
        self.player = Player(PLAYER_START_POS,[self.visible_sprites],self.obstacle_sprites)
        self.enemy = Enemy(mission_name,'1',ENEMY_START_POS, [self.visible_sprites],self.obstacle_sprites)
        self.enemies = [self.enemy] 
        self.death_counter = 0 
        self.stats = GameStats()
        self.paused_times = 0
        self.encounter_distance = 700
        self.reset_distance = 2000
        self.in_encounter_range = False
        self.was_far_away = True
        self.number_chases = 0
        self.in_chase_radius = False 
        self.heartbeat = Heartbeat()
        self.chase_start_time = None
        self.total_chase_time = 0

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
                                None
    def stats_screen(self, display_surface):
        screen_width, screen_height = 800, 600
        display_surface.fill((50, 50, 50))  

        stats_font = pygame.font.Font(None, 50)

        stats = [
            f"Pathfinding: {self.stats.pathfinding}",
            f"Time played: {self.stats.time_played}",
            f"Died: {self.stats.died}",
            f"Won: {self.stats.won}",
            f"Amount paused: {self.stats.amount_paused}",
            f"Escaped chases: {self.stats.chases_escaped}",
            f"Combined chase time: {self.stats.chase_times}",
            f"Average heartbeat: {self.stats.avg_heartbeat}"
        ]
        start_y = (screen_height - (len(stats) * 50)) / 2

        for i, stat in enumerate(stats):
            stats_text = stats_font.render(stat, True, (255, 255, 255))
            stats_text_rect = stats_text.get_rect(center=(screen_width / 2, start_y + i * 50))
            display_surface.blit(stats_text, stats_text_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: 
                        self.game_over_screen(display_surface)
                        break
            pygame.display.flip()


    def game_over_screen(self, display_surface):
        screen_width, screen_height = 800, 600

        display_surface.fill(BLACK)

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
                    if quit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
            pygame.display.flip()

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.heartbeat.update(self.player, self.enemy)
        self.heartbeat.draw(self.display_surface)

        chase_start_ticks = None  

        for enemy in self.enemies:
            distance = ((self.player.rect.x - enemy.rect.x)**2 + (self.player.rect.y - enemy.rect.y)**2)**0.5

            if pygame.sprite.collide_rect(self.player, enemy):
                if self.in_chase_radius: 
                    self.number_chases += 1  
                    self.total_chase_time += pygame.time.get_ticks() - self.chase_start_time
                self.stats.pathfinding =  self.enemy.enemy_type 
                self.stats.died = True 
                self.stats.won = False 
                self.stats.time_played = self.player.get_time_played()
                self.stats.amount_paused = self.paused_times
                self.stats.chases_escaped = self.number_chases
                self.stats.chase_times = self.total_chase_time / 1000 
                self.stats.avg_heartbeat = self.heartbeat.get_avg_heartbeat()
                self.stats_screen(self.display_surface)
                return
            elif distance > enemy.chase_radius:  
                if self.in_chase_radius: 
                    self.number_chases += 1  
                    self.in_chase_radius = False  
            elif distance <= enemy.chase_radius:
                if not self.in_chase_radius:  
                    self.chase_start_time = pygame.time.get_ticks()
                self.in_chase_radius = True