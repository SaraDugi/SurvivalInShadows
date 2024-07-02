import pygame


class Heartbeat:
    def __init__(self):
        self.heartbeat = 0 
        self.font = pygame.font.Font(None, 36) 
        self.total_heartbeat = 0 
        self.heartbeat_count = 0  
        self.lowest_heartbeat = float('inf')  
        self.highest_heartbeat = float('-inf') 

    def update(self, player, enemy):
        distance = ((player.rect.x - enemy.rect.x)**2 + (player.rect.y - enemy.rect.y)**2)**0.5

        if distance < 200:  
            self.heartbeat = 130 - (distance - 0) * (130 - 110) / (200 - 0)
        elif distance < 500:  
            self.heartbeat = 110 - (distance - 200) * (110 - 85) / (500 - 200)
        else:
            self.heartbeat = 85
        self.lowest_heartbeat = min(self.lowest_heartbeat, self.heartbeat)
        self.highest_heartbeat = max(self.highest_heartbeat, self.heartbeat)
        self.total_heartbeat += self.heartbeat
        self.heartbeat_count += 1

    def draw(self, screen):
        if self.heartbeat < 110:
            color = (0, 255, 0) 
        elif self.heartbeat < 130:
            color = (255, 165, 0)  
        else:
            color = (255, 0, 0)  

        text = self.font.render(str(int(self.heartbeat)), True, color)
        screen.blit(text, (10, 75))  

    def get_avg_heartbeat(self):
        return round(self.total_heartbeat / self.heartbeat_count, 2) if self.heartbeat_count else 0