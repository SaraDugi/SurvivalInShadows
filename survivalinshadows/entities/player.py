import pygame
from misc.settings import *
from misc.csvimport import import_folder
from entities.entity import *
from mechanisms.timer import Timer
from mechanisms.stamina import Stamina

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.character_path = "Graphics/Character_model/"
        self.image = pygame.image.load(f"{self.character_path}down_idle/down_1.PNG").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hit_box = self.rect.inflate(0, 0)
        self.import_player_assets()
        self.status = 'down'
        self.obstacle_sprites = obstacle_sprites
        self.stats = {'health': 250, 'speed': 3.00}
        self.health = self.stats['health']
        self.speed = self.stats['speed']
        self.health_bar = pygame.Rect(10, 10, self.health, 25)
        self.mood = 'normal'
        self.heartbeat_color = (0, 255, 0)
        self.heartbeat_ticks = 0
        self.total_distance_running = 0
        self.stamina = Stamina()
        self.timer = Timer(pygame.time.get_ticks())  

    def import_player_assets(self):
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': []
        }

        for animation in self.animations.keys():
            full_path = self.character_path + animation
            self.animations[animation] = import_folder(full_path)

    def check_collision(self, enemies):
        return self.collidelist(enemies) != -1

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

        if keys[pygame.K_TAB]:
            self.stamina.use_stamina()

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if 'idle' not in self.status:
                self.status += '_idle'

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hit_box.center)

    def update(self):
        self.input()
        self.get_status()
        self.animate()

        self.stamina.draw_stamina_items(pygame.display.get_surface())
        self.timer.draw_timer(pygame.display.get_surface())
        self.stamina.reset_speed_boost()

        if self.stamina.speed_boost_active:
            self.move(self.speed * 2)  
        else:
            self.move(self.speed)