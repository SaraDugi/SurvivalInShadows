import datetime
import math
import pygame 
from settings import *
from csvimport import import_folder
from entity import *
import pygame.gfxdraw 
from collections import Counter

class Player(Entity):
	def __init__(self,pos,groups,obstacle_sprites):
		super().__init__(groups)
		self.image = pygame.image.load('Graphics/Character_model/down_idle/down_1.PNG').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hit_box = self.rect.inflate(0,0)
		self.import_player_assets()
		self.status = 'down'
		self.obstacle_sprites = obstacle_sprites
		self.stats = {'health': 250, 'stamina':150, 'speed':2}
		self.health = self.stats['health']
		self.energy = self.stats['stamina']
		self.speed = self.stats['speed']
		self.health_bar = pygame.Rect(10, 10, self.health, 25) 
		self.stamina_bar = pygame.Rect(10, 40, self.energy, 25)
		self.last_stamina_reduction = pygame.time.get_ticks() 
		self.speed_boost_active = False  
		self.last_speed_boost = 0 
		self.start_ticks = pygame.time.get_ticks()  
		self.mood = 'normal'
		self.heartbeat_color = (0, 255, 0) 
		self.heartbeat_ticks = 0 
		self.total_distance_running = 0

	def import_player_assets(self):
		character_path = 'Graphics/Character_model/'
		self.animations = {'up': [],'down': [],'left': [],'right': [],
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def check_collision(self, enemies):
		if self.collidelist(enemies)!= -1:
			return True
		return False
	
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
			current_time = pygame.time.get_ticks()
			if current_time - STAMINA_COOLDOWN >= STAMINA_COOLDOWN:  
				self.energy -= STAMINA_REDUCTION  
				self.stamina_bar.width = self.energy
				self.last_stamina_reduction = current_time  
				self.speed_boost_active = True  
				self.last_speed_boost = current_time  
	
	def get_status(self):
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status in self.status:
				self.status = self.status + '_idle'

	def draw_timer(self, screen):
		total_seconds = 600 - (pygame.time.get_ticks() - self.start_ticks) / 1000  
		if total_seconds < 0:
			total_seconds = 0
		minutes = total_seconds // 60
		seconds_in_minute = total_seconds % 60
		milliseconds = (total_seconds % 1) * 1000
		font = pygame.font.SysFont("monospace", 50, bold=True)
		text = f"{int(minutes)}:{int(seconds_in_minute):02}:{int(milliseconds):03}"
		
		text_surface = font.render(text, True, (255, 255, 255))
		text_rect = text_surface.get_rect(center=(screen.get_width() // 2, 50))
		screen.blit(text_surface, text_rect)

	def get_time_played(self):
		total_seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
		playtime = datetime.timedelta(seconds=int(total_seconds))
		time_played = str(playtime).split('.')[0]
		return time_played
	
	def animate(self):
		animation = self.animations[self.status]

		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hit_box.center)

	def update_health_bar(self, screen):
		pygame.draw.rect(screen, (255,0,0), self.health_bar)

	def update_stamina_bar(self, screen):
		pygame.draw.rect(screen, (0,255,0), self.stamina_bar)
		
	def update(self):
		self.input()
		self.get_status()
		self.animate()
		self.move(self.speed)
		self.draw_timer(pygame.display.get_surface())
		self.update_health_bar(pygame.display.get_surface())
		self.update_stamina_bar(pygame.display.get_surface())
			 
		if self.speed_boost_active and pygame.time.get_ticks() - self.last_speed_boost <= SPEED_BOOST_DURATION:
			self.move(self.speed * 2)  
			self.previous_player_position = self.rect.topleft 
		else:
			self.speed_boost_active = False  
			self.move(2)