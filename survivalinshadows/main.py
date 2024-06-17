import pygame
import sys
from level import Level
from settings import *
from player import *
import os
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Survival in Shadows')
font = pygame.font.SysFont(None, FONT_SIZE)

class Menu:
    def __init__(self, title, options):
        self.title = title
        self.options = options
        self.selected_option = 0

    def render(self):
        screen.fill(BLACK)
        title_text = font.render(self.title, True, GREEN)
        title_rect = title_text.get_rect(center=(WIDTH / 2, HEIGHT / 4))
        screen.blit(title_text, title_rect)
        
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                text = font.render(option, True, GREEN)
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

def load_game(mission_name):
    level = Level(mission_name) 
    clock = pygame.time.Clock()

    if mission_name == 'Mission 1':
            level.enemy.enemy_type = 'astar'
    elif mission_name == 'Mission 2':
            level.enemy.enemy_type = 'bfs'
    elif mission_name == 'Mission 3':
            level.enemy.enemy_type = 'decisiontree'
    elif mission_name == 'Mission 4':
            level.enemy.enemy_type = 'geneticalal'
    elif mission_name == 'Mission 5':
            level.enemy.enemy_type = 'knn'

    print(f"Selected mission: {mission_name}")
    print(f"Enemy type: {level.enemy.enemy_type}")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        level.run()  
        '''path = level.enemy.enemy_move(level.player)  
        if path is not None: 
            print(path) '''
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