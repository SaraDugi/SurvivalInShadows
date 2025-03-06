import pygame
import math
from misc.settings import *
from entities.entity import *
from misc.csvimport import *
from pathfinding.astar import astar_pathfinding
from pathfinding.bfs import bfs_pathfinding
from pathfinding.dijsktra import dijkstra_pathfinding
from pathfinding.greedy import greedy_pathfinding
from pathfinding.bidirectional import bidirectional_pathfinding

class Enemy(Entity):
    def __init__(self, enemy_type, name, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.enemy_type = enemy_type
        self.import_graphics(name)
        self.status = 'walk'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.hit_box = self.rect.inflate(0, 0)
        self.obstacle_sprites = obstacle_sprites
        self.frame_index = 0 
        self.monster_name = name

        monster_info = monster_data[self.monster_name]
        self.speed = monster_info['speed']
        self.attack_damage = None 
        self.chase_radius = monster_info['chase_radius']
        self.notice_radius = monster_info['notice_radius']
        
        self.attack_cooldown = 1000
        self.last_attack_time = 0

    def import_graphics(self, name):
        self.animations = {'walk': [], 'chase': []}
        main_path = f'Graphics/Enemy_models/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        if distance <= self.chase_radius:
            self.status = 'chase'
            self.speed = self.speed * 2  
        else:
            self.status = 'walk'
            self.speed = 3

    def attack(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > self.attack_cooldown:
            if not player.invincible:  
                damage = player.stats['health'] * 0.1
                player.take_damage(damage)
                self.last_attack_time = current_time  

    def enemy_move(self, player):
        maze = read_csv_file('Graphics/Map/CSV/abandonefactory_limit.csv')  
        start = (int(self.rect.x // TILESIZE), int(self.rect.y // TILESIZE))
        end = (int(player.rect.x // TILESIZE), int(player.rect.y // TILESIZE))
        path = None

        if self.rect.x % TILESIZE == 0 and self.rect.y % TILESIZE == 0:
            if self.enemy_type == 'a*':
                path = astar_pathfinding(maze, start, end, MAX_STEPS) 
            elif self.enemy_type == 'bfs':
                path = bfs_pathfinding(maze, start, end, MAX_STEPS)
            elif self.enemy_type == 'd':
                path = dijkstra_pathfinding(maze, start, end, MAX_STEPS)
            elif self.enemy_type == 'greedy':
                path = greedy_pathfinding(maze, start, end, MAX_STEPS)
            elif self.enemy_type == 'bd':
                path = bidirectional_pathfinding(maze, start, end, MAX_STEPS)
            
            if path is not None and len(path) > 1:  # Ensure path has at least 2 elements
                next_step = list(path[1])
                next_step[0] *= TILESIZE
                next_step[1] *= TILESIZE
                self.direction = pygame.math.Vector2(next_step[0] - self.rect.x, next_step[1] - self.rect.y)
            else:
                self.direction = pygame.math.Vector2(0, 0)  # Stop moving if no valid path

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        return (distance, direction)

    def actions(self, player):
        if self.status == 'walk':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()
    
    def animate(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hit_box.center)

    def enemy_update(self, player):
        self.get_status(player)
        if not pygame.sprite.collide_rect(self, player):  # Move only if not colliding
            self.enemy_move(player)
        self.animate()

        if pygame.sprite.collide_rect(self, player):
            self.attack(player)
            self.direction = pygame.math.Vector2(0, 0)  # Stop enemy movement