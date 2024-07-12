import math
import sys
import pygame
import requests
from tkinter import font
from settings import *
from csvimport import import_csv_layout
from enemy import Enemy
from game_stats import GameStats
from camera import YSortCameraGroup
from heartbeat import Heartbeat
from tile import Tile
from player import Player

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_RED = (139, 0, 0)  
GHOST_WHITE = (248, 248, 255)  


class Level:
    url = "https://survivalinshadowsbackend.onrender.com/game-data"
    
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
        self.previous_player_position = self.player.rect.topleft  
        self.previous_enemy_position = self.enemy.rect.topleft  
        self.path_efficiency = 0
        self.nodes_explored = 0 
        self.start_ticks = pygame.time.get_ticks()  

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

        if self.stats.died:
            message_text = "Game Over"
            message_color = DARK_RED
        else:
            message_text = "Victory!"
            message_color = GHOST_WHITE

        message_font = pygame.font.Font(None, 100)  
        message_surface = message_font.render(message_text, True, message_color)
        message_rect = message_surface.get_rect(center=(screen_width / 2, screen_height / 2))

        display_surface.blit(message_surface, message_rect)

        buttons = []
        for i, option in enumerate(GAMEOVER_OPTIONS):
            button = pygame.Rect(screen_width / 2 - button_width / 2, screen_height / 2 + 150 + i * (button_height + 20), button_width, button_height)  # Adjust position below the message
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
        self.visible_sprites.enemy_update(self.player, self.stats)
        self.heartbeat.update(self.player, self.enemy)
        self.heartbeat.draw(self.display_surface)
        for enemy in self.enemies:
            distance = ((self.player.rect.x - enemy.rect.x)**2 + (self.player.rect.y - enemy.rect.y)**2)**0.5

            if pygame.sprite.collide_rect(self.player, enemy):
                if self.in_chase_radius: 
                    self.number_chases += 1  
                    self.total_chase_time += pygame.time.get_ticks() - self.chase_start_time
                self.stats.pathfinding =  self.enemy.enemy_type 
                self.stats.died = True 
                self.stats.won = False 
                self.stats.stamina_used = self.player.used_stamina
                self.stats.time_played = self.player.get_time_played()
                self.stats.amount_paused = self.paused_times
                self.stats.chases_escaped = self.number_chases
                self.stats.chase_times = self.total_chase_time / 1000 
                self.stats.avg_heartbeat = self.heartbeat.get_avg_heartbeat()
                self.stats.most_often_mood = self.heartbeat.get_mostoften_mood()
                self.stats.rarest_mood = self.heartbeat.rarest_mood()
                self.stats.total_distance_travelled += math.sqrt((self.player.rect.x - self.previous_player_position[0])**2 + (self.player.rect.y - self.previous_player_position[1])**2)
                self.previous_player_position = self.player.rect.topleft 
                self.stats.pathfinding_length += math.sqrt((self.enemy.rect.x - self.previous_enemy_position[0])**2 + (self.enemy.rect.y - self.previous_enemy_position[1])**2)
                self.previous_enemy_position = self.enemy.rect.topleft
                self.stats.total_enemy_distance_travelled_sprint = self.enemy.total_distance_while_player_sprints
                self.send_data_to_server()
                self.game_over_screen(self.display_surface)
                return
            elif distance > enemy.chase_radius:  
                if self.in_chase_radius: 
                    self.number_chases += 1  
                    self.in_chase_radius = False  
            elif distance <= enemy.chase_radius:
                if not self.in_chase_radius:  
                    self.chase_start_time = pygame.time.get_ticks()
                self.in_chase_radius = True

        total_seconds = 300 - (pygame.time.get_ticks() - self.start_ticks) / 1000  
        if total_seconds <= 0:
            if self.in_chase_radius: 
                self.number_chases += 1  
                self.total_chase_time += pygame.time.get_ticks() - self.chase_start_time
            self.stats.pathfinding =  self.enemy.enemy_type 
            self.stats.died = False 
            self.stats.won = True 
            self.stats.stamina_used = self.player.used_stamina
            self.stats.time_played = self.player.get_time_played()
            self.stats.amount_paused = self.paused_times
            self.stats.chases_escaped = self.number_chases
            self.stats.chase_times = self.total_chase_time / 1000 
            self.stats.avg_heartbeat = self.heartbeat.get_avg_heartbeat()
            self.stats.most_often_mood = self.heartbeat.get_mostoften_mood()
            self.stats.rarest_mood = self.heartbeat.rarest_mood()
            self.stats.total_distance_travelled += math.sqrt((self.player.rect.x - self.previous_player_position[0])**2 + (self.player.rect.y - self.previous_player_position[1])**2)
            self.previous_player_position = self.player.rect.topleft 
            self.stats.pathfinding_length += math.sqrt((self.enemy.rect.x - self.previous_enemy_position[0])**2 + (self.enemy.rect.y - self.previous_enemy_position[1])**2)
            self.previous_enemy_position = self.enemy.rect.topleft
            self.stats.total_enemy_distance_travelled_sprint = self.enemy.total_distance_while_player_sprints
            self.send_data_to_server()
            self.game_over_screen(self.display_surface)
            return

    def send_data_to_server(self):
        game_data = {
            # Player stats
            "timePlayed" : self.stats.time_played,
            "died": self.stats.died,
            "won": self.stats.won,
            "amountPaused": self.stats.amount_paused,
            "encounters": self.stats.encounters,
            "escapedChases": self.stats.chases_escaped,
            "averageHeartbeat": self.stats.avg_heartbeat,
            "mostOftenHeartbeat": self.stats.most_often_mood,
            "rarestHeartbeat": self.stats.rarest_mood,
            "totalDistanceTraveled": f"{round(self.stats.total_distance_travelled, 2)} pixels",
            "staminaUsed": self.stats.stamina_used,
            "playerDistanceSprinted": self.stats.player_distance_sprinted,

            # Enemy stats
            "pathFinding": self.stats.pathfinding,
            "combinedChaseTime": self.stats.chase_times,
            "pathFindingLength": self.stats.pathfinding_length,
            "totalEnemyDistanceTravelledSprint": self.stats.total_enemy_distance_travelled_sprint,
            "nodesExplored": self.stats.nodes_explored
        }

        response = requests.post(self.url, json = game_data)
        print(game_data)
        print(response.text)
            