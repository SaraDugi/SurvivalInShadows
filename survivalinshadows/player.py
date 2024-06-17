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
		self.stats = {'stamina':100, 'speed':2}
		self.energy = self.stats['stamina']
		self.speed = self.stats['speed']
		self.stamina_index = 0
		self.stamina_bar = pygame.Rect(10, 10, self.energy, 25)
		self.stamina_reduction = 10  
		self.stamina_cooldown = 1000  
		self.last_stamina_reduction = pygame.time.get_ticks() 
		self.speed_boost_active = False  
		self.speed_boost_duration = 5000 
		self.last_speed_boost = 0 

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
			if current_time - self.last_stamina_reduction >= self.stamina_cooldown:  
				self.energy -= self.stamina_reduction  
				self.stamina_bar.width = self.energy
				self.last_stamina_reduction = current_time  
				self.speed_boost_active = True  
				self.last_speed_boost = current_time  
	
	def get_status(self):
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status in self.status:
				self.status = self.status + '_idle'

	def draw_stamina_bar(self, screen):
		pygame.draw.rect(screen, (255, 0, 0), self.stamina_bar)

	def animate(self):
		animation = self.animations[self.status]

		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hit_box.center)

	def update(self):
		self.input()
		self.get_status()
		self.animate()
		self.move(self.speed)
		self.draw_stamina_bar(pygame.display.get_surface()) 

		if self.speed_boost_active and pygame.time.get_ticks() - self.last_speed_boost <= self.speed_boost_duration:
			self.move(self.speed * 2)  
		else:
			self.speed_boost_active = False  
			self.move(self.speed)
		self.draw_stamina_bar(pygame.display.get_surface())
