import pygame
from misc.settings import *
from misc.csvimport import import_folder
from entities.entity import Entity
from mechanisms.timer import Timer
from mechanisms.stamina import Stamina
from mechanisms.healthbar import HealthBar
from mechanisms.inventory import Inventory

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
        self.stamina = Stamina()
        self.timer = Timer(pygame.time.get_ticks())  
        self.health_bar = HealthBar(self)  
        self.invincible = False
        self.last_hit_time = 0
        self.invincibility_duration = 1000
        self.inventory = Inventory()

    def import_player_assets(self):
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': []
        }
        for animation in self.animations.keys():
            full_path = self.character_path + animation
            self.animations[animation] = import_folder(full_path)

    def take_damage(self, amount):
        current_time = pygame.time.get_ticks()
        if not self.invincible:
            self.health = max(0, self.health - amount)
            self.invincible = True
            self.last_hit_time = current_time
        if self.health <= 0:
            self.die()

    def heal(self, amount):
        self.health = min(self.stats['health'], self.health + amount)

    def die(self):
        print("💀 Player has died!")

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'

        if keys[pygame.K_TAB]:
            self.stamina.use_stamina()

        # Toggle inventory with I key.
        if keys[pygame.K_i]:
            self.inventory.toggle_inventory()

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
        self.health_bar.update()
        self.stamina.reset_speed_boost()

        if self.invincible and pygame.time.get_ticks() - self.last_hit_time > self.invincibility_duration:
            self.invincible = False

        if self.stamina.speed_boost_active:
            self.move(self.speed * 2)
        else:
            self.move(self.speed)

    def draw_ui(self, screen, font):
        self.health_bar.draw(screen)
        self.stamina.draw_stamina_items(screen)
        self.timer.draw_timer(screen)
        self.inventory.render_inventory_screen(screen, font)