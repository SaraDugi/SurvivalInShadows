import pygame
import datetime

class Timer:
    def __init__(self, start_ticks, countdown_time=300):
        self.start_ticks = start_ticks
        self.countdown_time = countdown_time

    def draw_timer(self, screen):
        total_seconds = self.countdown_time - (pygame.time.get_ticks() - self.start_ticks) / 1000  
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
        return str(playtime).split('.')[0]