import pygame
from misc.settings import *

class Stamina:
    def __init__(self, initial_stamina=3):
        self.max_stamina = initial_stamina
        self.stamina_counter = initial_stamina
        self.speed_boost_active = False
        self.last_speed_boost = 0
        self.used_stamina = 0

    def use_stamina(self):
        current_time = pygame.time.get_ticks()
        if self.stamina_counter > 0 and not self.speed_boost_active:
            if current_time - self.last_speed_boost >= STAMINA_COOLDOWN:
                self.last_speed_boost = current_time
                self.stamina_counter -= 1
                self.speed_boost_active = True
                self.used_stamina += 1

    def reset_speed_boost(self):
        if self.speed_boost_active and pygame.time.get_ticks() - self.last_speed_boost > SPEED_BOOST_DURATION:
            self.speed_boost_active = False

    def draw_stamina_items(self, screen):
        stamina_pos = (10, 10)
        font = pygame.font.Font(None, 36)
        text = "Stamina usage left: "
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (stamina_pos[0], stamina_pos[1]))

        if self.stamina_counter > 2:
            color = (0, 255, 0)
        elif self.stamina_counter > 1:
            color = (255, 165, 0)
        else:
            color = (255, 0, 0)

        counter_surface = font.render(str(self.stamina_counter), True, color)
        screen.blit(counter_surface, (stamina_pos[0] + text_surface.get_width(), stamina_pos[1]))