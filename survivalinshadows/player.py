import datetime
import math
import pygame 
from settings import *
from csvimport import import_folder
from entity import *
import pygame.gfxdraw 

class Player(Entity):
	def __init__(self,pos,groups,obstacle_sprites):
		super().__init__(groups)
		self.image = pygame.image.load('Graphics/Character_model/down_idle/down_1.PNG').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hit_box = self.rect.inflate(0,0)
		self.import_player_assets()
		self.status = 'down'
		self.obstacle_sprites = obstacle_sprites
		self.stats = {'health': 250, 'stamina':100, 'speed':2}
		self.health = self.stats['health']
		self.energy = self.stats['stamina']
		self.speed = self.stats['speed']
		self.health_bar = pygame.Rect(10, 40, self.health, 25) 
		self.stamina_index = 0
		self.stamina_bar = pygame.Rect(10, 10, self.energy, 25)
		self.last_stamina_reduction = pygame.time.get_ticks() 
		self.speed_boost_active = False  
		self.last_speed_boost = 0 
		self.start_ticks = pygame.time.get_ticks()  
		self.mood = 'normal'

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

	def draw_stats(self, screen):
		font = pygame.font.SysFont(None, 36)
		colors = {'normal': (0, 255, 0), 'stressed': (255, 165, 0), 'critical': (255, 0, 0)}
		positions = [(10, 10), (10, 50), (10, 90), (10, 130)]

		elements = [
			{'type': 'rect', 'color': (255, 0, 0), 'rect': self.health_bar, 'order': 2},
			{'type': 'rect', 'color': (0, 0, 255), 'rect': self.stamina_bar, 'order': 1},
			{'type': 'text', 'text': 'Mood: ' + self.mood.capitalize(), 'color': colors[self.mood], 'pos': positions[2], 'order': 3}
		]

		elements.sort(key=lambda x: x['order'])

		for element in elements:
			if element['type'] == 'rect':
				pygame.draw.rect(screen, element['color'], element['rect'])
			elif element['type'] == 'text':
				text = font.render(element['text'], True, element['color'])
				screen.blit(text, element['pos'])

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
		time_played = str(datetime.timedelta(seconds=int(total_seconds)))
		return time_played

	def animate(self):
		animation = self.animations[self.status]

		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hit_box.center)
	
	def update_heartbeat(self):
		if self.mood == 'normal':
			self.heartbeat_value = 10
		elif self.mood == 'stressed':
			self.heartbeat_value = 20
		else:  
			self.heartbeat_value = 30
		
	def update(self):
		self.input()
		self.get_status()
		self.animate()
		self.move(self.speed)
		self.health_bar.width = self.health
		self.draw_stats(pygame.display.get_surface()) 
		self.draw_timer(pygame.display.get_surface())

		if self.speed_boost_active and pygame.time.get_ticks() - self.last_speed_boost <= SPEED_BOOST_DURATION:
			self.move(self.speed * 2)  
		else:
			self.speed_boost_active = False  
			self.move(self.speed)