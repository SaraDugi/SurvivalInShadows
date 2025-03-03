import pygame
import sys
from levels.level import Level
from misc.settings import *
from menus.menu import Menu
from menus.pausemenu import PauseMenu
from menus.startscreen import StartScreen

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

def load_game(mission_name):
    is_torch_effect = False
    level = Level(mission_name)
    clock = pygame.time.Clock()

    pause_menu = PauseMenu('Paused', ['Resume', 'Quit Game'], mission_name, level, screen, font)
    paused = False

    start_menu_music.stop()
    game_music.play(-1) 
    game_music.set_volume(0.4)

    if mission_name == 'Mission 1':
        level.enemy.enemy_type = 'a*'

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
            pause_menu.render()
        else:
            level.run(is_torch_effect)
            pygame.display.flip()
            clock.tick(60)

def main():
    running = True
    
    start_menu = Menu("Survival in Shadows", MAIN_OPTIONS, screen, font)
    mission_menu = Menu("Survival in Shadows", MISSION_OPTIONS, screen, font)
    current_menu = start_menu

    start_menu_music.play(-1)

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
                        print(f"{mission_name} selected!")
                        
                        start_screen = StartScreen(
                            "Survive for the longest you can!",
                            [
                                "",
                                "",
                                "",
                                "Arrow keys for moving",
                                "TAB for sprint",
                                "",
                                "",
                                "Press SPACE to start the game"
                            ],
                            screen,
                            font
                        )
                        show_start = True
                        while show_start:
                            event2 = pygame.event.wait()
                            show_start = start_screen.handle_event(event2)
                            start_screen.render()

                        load_game(mission_name)
                        current_menu = start_menu
                else:
                    current_menu.handle_event(event)

        current_menu.render()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()