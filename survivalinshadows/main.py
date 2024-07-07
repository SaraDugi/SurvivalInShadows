import pygame
import sys
from level import *
from settings import *
from player import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Survival in Shadows')
pygame.font.init() 
pygame.mixer.init()
font = pygame.font.SysFont(None, FONT_SIZE)
background = pygame.image.load('Graphics/Misc/menubackground-main.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
start_menu_music = pygame.mixer.Sound('Graphics/Audio/bg_audio/2. Moonless Night.wav')
game_music = pygame.mixer.Sound('Graphics/Audio/bg_audio/6. Lurking in the Dark.wav')

class Menu:
    def __init__(self, title, options):
        self.title = title
        self.options = options
        self.selected_option = 0

    def render(self):
        screen.blit(background, (0, 0))
        title_text = font.render(self.title, True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH / 2, HEIGHT / 4))
        screen.blit(title_text, title_rect)
        
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                text = font.render(option, True, RED)
            else:
                text = font.render(option, True, WHITE)
            text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + i * 60))
            screen.blit(text, text_rect)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.selected_option > 0:
                self.selected_option -= 1
            elif event.key == pygame.K_DOWN and self.selected_option < len(self.options) - 1:
                self.selected_option += 1

class StartScreen(Menu):
    def __init__(self, title, instructions):
        super().__init__(title, [])
        self.instructions = instructions

    def render(self):
        screen.fill((0, 0, 0))  
        title_text = font.render(self.title, True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH / 2, HEIGHT / 4))
        screen.blit(title_text, title_rect)
        
        for i, instruction in enumerate(self.instructions):
            text = font.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + (i - len(self.instructions) / 2) * 60))
            screen.blit(text, text_rect)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            return False
        return True

class PauseMenu(Menu):
    def __init__(self, title, options, mission_name,level):
        super().__init__(title, options)
        self.mission_name = mission_name
        self.level = level

    def handle_event(self, event, level):
        screen.fill(BLACK)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.selected_option > 0:
                self.selected_option -= 1
            elif event.key == pygame.K_DOWN and self.selected_option < len(self.options) - 1:
                self.selected_option += 1
            elif event.key == pygame.K_RETURN:
                if self.options[self.selected_option] == 'Resume':
                    return False
                elif self.options[self.selected_option] == 'Quit Game':
                    pygame.quit()
                    sys.exit()
                elif self.options[self.selected_option] == 'Quit to Title':
                    return 'main_menu'
        return True

def load_game(mission_name):
    level = Level(mission_name) 
    clock = pygame.time.Clock()
    pause_menu = PauseMenu('Paused', ['Resume', 'Quit Game', 'Quit to Title'], mission_name, level)
    paused = False
    start_menu_music.stop()
    game_music.play()
    game_music.set_volume(0.4)

    if mission_name == 'Mission 1':
            level.enemy.enemy_type = 'a*'
    elif mission_name == 'Mission 2':
            level.enemy.enemy_type = 'd'
    elif mission_name == 'Mission 3':
            level.enemy.enemy_type = 'bfs'
    elif mission_name == 'Mission 4':
            level.enemy.enemy_type = 'g'
    elif mission_name == 'Mission 5':
            level.enemy.enemy_type = 'bd'

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                if paused:
                    paused = pause_menu.handle_event(event, level)
        if paused:
            if paused == 'main_menu':
                return
            pause_menu.render()
        else:
            level.run()  
            pygame.display.flip() 
            clock.tick(60)
        
def main():
    running = True
    start_menu = Menu("Survival in Shadows", MAIN_OPTIONS)
    mission_menu = Menu("Survival in Shadows", MISSION_OPTIONS)
    current_menu = start_menu

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if current_menu == start_menu:
                        if current_menu.selected_option == 0:
                            current_menu = mission_menu
                        else:
                            pygame.quit()
                            sys.exit()
                    elif current_menu == mission_menu:
                        mission_name = f"Mission {current_menu.selected_option + 1}"
                        print(mission_name + " selected!")
                        
                        start_screen = StartScreen("Survive for the longest you can!", [
                            '',
                            '',
                            "Controls:",
                            "Arrow keys for moving",
                            "TAB for sprint",
                            '',
                            '',
                            "Press SPACE to start the game"
                        ])
                        while start_screen.handle_event(pygame.event.wait()):
                            start_screen.render()
                        
                        load_game(mission_name)
                        current_menu = start_menu
                else:
                    current_menu.handle_event(event)

        current_menu.render()
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()