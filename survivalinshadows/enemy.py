import pygame
from settings import *
from entity import *
from csvimport import *
from pathfidning_astar import  astar_pathfinding
from pathfidning_bfs import bfs_pathfinding
from pathfinding_dijsktra import dijkstra_pathfinding
import sys
from pathfidning_greedy import greedy_pathfinding
from pathfidning_bidirectional import bidirectional_pathfinding

class Enemy(Entity):
    def __init__(self,enemy_type,name, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.enemy_type = enemy_type
        self.import_graphics(name)
        self.status = 'walk'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.rect = self.image.get_rect(topleft = pos)
        self.hit_box = self.rect.inflate(0, 0)
        self.obstacle_sprites = obstacle_sprites
        self.frame_index = 0 
        self.monster_name = name
        monster_info = monster_data[self.monster_name]
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.chase_radius = monster_info['chase_radius']
        self.notice_radius = monster_info['notice_radius']
        self.next = None
        self.nodes_explored = 0

    def import_graphics(self,name):
        self.animations = {'walk' : [], 'chase': []}
        main_path = f'Graphics/Enemy_models/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_status(self,player):
        distance = self.get_player_distance_direction(player)[0]
        if distance <= self.notice_radius:
            self.status = 'chase'
        else:
            self.status = 'walk'

    def enemy_move(self, player):
        maze = read_csv_file('Graphics/Map/CSV/abandonefactory_limit.csv')  
        start = (int(self.rect.x//TILESIZE), int(self.rect.y//TILESIZE))
        end = (int(player.rect.x//TILESIZE), int(player.rect.y//TILESIZE))
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
            
            if path is not None and len(path) > 0:
                next_step = list(path[1])
                next_step[0] *= TILESIZE
                next_step[1] *= TILESIZE
                self.direction = pygame.math.Vector2(next_step[0] - self.rect.x, next_step[1] - self.rect.y)
        
        if path != None or self.rect.x % TILESIZE != 0 or self.rect.y % TILESIZE != 0:
            self.move(3)
        
    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        return (distance,direction)
    
    def actions(self,player):
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
        self.rect = self.image.get_rect(center = self.hit_box.center)

    def enemy_update(self,player):
        self.get_status(player)
        self.enemy_move(player) 
        self.animate()
