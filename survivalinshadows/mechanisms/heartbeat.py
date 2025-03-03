import pygame
from collections import Counter

class Heartbeat:
    def __init__(self):
        self.heartbeat = 0 
        self.font = pygame.font.Font(None, 36) 
        self.total_heartbeat = 0 
        self.heartbeat_count = 0  
        self.lowest_heartbeat = float('inf')  
        self.highest_heartbeat = float('-inf') 
        self.moods = []

    def update(self, player, enemy):
        distance = ((player.rect.x - enemy.rect.x)**2 + (player.rect.y - enemy.rect.y)**2)**0.5

        if distance < 200:  
            self.heartbeat = 140 - (distance - 0) * (140 - 95) / (200 - 0)
        elif distance < 500:  
            self.heartbeat = 95 - (distance - 200) * (95 - 85) / (500 - 200)
        else:
            self.heartbeat = 65
        self.lowest_heartbeat = min(self.lowest_heartbeat, self.heartbeat)
        self.highest_heartbeat = max(self.highest_heartbeat, self.heartbeat)
        self.total_heartbeat += self.heartbeat
        self.heartbeat_count += 1
        self.moods.append(self.get_mood())

    def draw(self, screen):
        if self.heartbeat < 95:
            color = (0, 255, 0)  
        elif self.heartbeat < 140:
            color = (255, 165, 0)  
        else:
            color = (255, 0, 0)

        text = "Heartbeat: "
        text_surface = self.font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 45))
        heartbeat_surface = self.font.render(str(int(self.heartbeat)), True, color)
        screen.blit(heartbeat_surface, (10 + text_surface.get_width(), 45))


    def get_avg_heartbeat(self):
        return round(self.total_heartbeat / self.heartbeat_count, 2) if self.heartbeat_count else 0

    def get_mood(self):
        if 65 <= self.heartbeat < 95:
            return "normal"
        elif 95 <= self.heartbeat < 140:
            return "alarmed"
        else: 
            return "panicked"

    def get_mostoften_mood(self):
        mood_counts = Counter(self.moods)
        most_common_mood, _ = mood_counts.most_common(1)[0]
        return most_common_mood

    def rarest_mood(self):
        mood_counts = Counter(self.moods)
        rarest_mood, _ = mood_counts.most_common()[-1]
        return rarest_mood