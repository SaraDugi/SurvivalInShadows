import pygame
from misc.settings import BLACK, WHITE

class HealthBar:
    def __init__(self, player):
        self.player = player
        self.max_health = player.stats['health']
        self.current_health = player.health
        self.width = 200 
        self.height = 25  
        self.border_thickness = 3
        self.x = 20
        self.y = 20  

    def update(self):
        self.current_health = self.player.health

    def draw(self, screen):
        # Draw the border.
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), border_radius=5)
        # Calculate the ratio for the health bar.
        health_ratio = max(0, self.current_health / self.max_health)
        # Choose the color based on the ratio.
        if health_ratio < 0.3:
            health_color = (255, 0, 0)
        elif health_ratio < 0.6:
            health_color = (255, 165, 0)
        else:
            health_color = (0, 255, 0)
        # Draw the health bar.
        pygame.draw.rect(screen, health_color, (self.x, self.y, self.width * health_ratio, self.height), border_radius=5)
        # Draw the border outline.
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), self.border_thickness, border_radius=5)