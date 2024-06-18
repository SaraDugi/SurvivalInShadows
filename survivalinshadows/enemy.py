import pygame
from settings import *
from entity import *
from csvimport import *
from pathfidning_astar import  astar_pathfinding
from pathfidning_ga import ga_pathfinding
from pathfidning_bfs import bfs_pathfinding
from pathfidning_decisiontrees import decisiontree_pathfinding
from pathfidning_knn import knn_pathfinding

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
        self.hit_box = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites
        self.frame_index = 0 
            
        self.monster_name = name
        monster_info = monster_data[self.monster_name]
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.chase_radius = monster_info['chase_radius']
        self.notice_radius = monster_info['notice_radius']
        self.pathfinding_methods = {
                    'astar': astar_pathfinding,
                    'geneticalal': ga_pathfinding,
                    'bfs': bfs_pathfinding,
                    'decisiontree': decisiontree_pathfinding,
                    'knn': knn_pathfinding,
                    'default': bfs_pathfinding
                }
        
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
        start = (int(self.rect.centerx//TILESIZE), int(self.rect.centery//TILESIZE))
        end = (int(player.rect.centerx//TILESIZE), int(player.rect.centery//TILESIZE))
        maze = read_csv_file('Graphics/Map/CSV/abandonefactory_limit.csv')  
        
        if self.enemy_type == 'a*':
            path = astar_pathfinding(maze, start, end)
            if path is not None and len(path) > 1:
                next_step = list(path[1])
                next_step[0] *= TILESIZE
                next_step[1] *= TILESIZE
                self.direction = pygame.math.Vector2(next_step[0] - self.rect.x, next_step[1] - self.rect.y)
                self.move(3)  
            else:
                self.direction = pygame.math.Vector2()
        if self.enemy_type == 'ga':
            path = ga_pathfinding(maze, start, end)
            if path is not None and len(path) > 0:
                next_step = list(path[0])
                next_step[0] *= TILESIZE
                next_step[1] *= TILESIZE
                self.direction = pygame.math.Vector2(next_step[0]  - self.rect.centerx, next_step[1] - self.rect.centery)
                self.move(3)
            else:
                self.direction = pygame.math.Vector2()
        if self.enemy_type == 'bfs':
            path = bfs_pathfinding(maze, start, end)
            if path is not None and len(path) > 0:
                next_step = list(path[0])
                next_step[0] *= TILESIZE
                next_step[1] *= TILESIZE
                self.direction = pygame.math.Vector2(next_step[0] - self.rect.x, next_step[1] - self.rect.y)
                self.move(3)
            else:
                self.direction = pygame.math.Vector2()
        if self.enemy_type == 'dt':
            path = decisiontree_pathfinding(maze, start, end)
            if path is not None and len(path) > 0:
                next_step = list(path[0])
                next_step[0] *= TILESIZE
                next_step[1] *= TILESIZE
                self.direction = pygame.math.Vector2(next_step[0] - self.rect.x, next_step[1] - self.rect.y)
                self.move(3)
            else:
                self.direction = pygame.math.Vector2()
        if self.enemy_type == 'knn':
            path = knn_pathfinding(maze, start, end, k=3)
            if path is not None and len(path) > 0:
                next_step = list(path[0])
                next_step[0] *= TILESIZE
                next_step[1] *= TILESIZE
                self.direction = pygame.math.Vector2(next_step[0] - self.rect.x, next_step[1] - self.rect.y)
                self.move(3)
            else:
                self.direction = pygame.math.Vector2()

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
        self.actions(player)
        self.enemy_move(player) 
        self.animate()
  