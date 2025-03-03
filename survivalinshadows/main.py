import pygame
import sys
from levels.level import Level
from misc.settings import *
from misc.settingsmanager import SettingsManager
from menus.menu import Menu
from menus.pausemenu import PauseMenu
from menus.startscreen import StartScreen

pygame.init()
settings_manager = SettingsManager()

screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h

fullscreen_flag = pygame.FULLSCREEN if settings_manager.get_setting("fullscreen") else 0
screen = pygame.display.set_mode((screen_width, screen_height), fullscreen_flag)

pygame.display.set_caption("Survival in Shadows")
pygame.font.init()
pygame.mixer.init()
font = pygame.font.SysFont(None, FONT_SIZE)

background = pygame.image.load("Graphics/Misc/menubackground-main.jpg")
background = pygame.transform.scale(background, (screen_width, screen_height))

start_menu_music = pygame.mixer.Sound("Graphics/Audio/bg_audio/2. Moonless Night.wav")
game_music = pygame.mixer.Sound("Graphics/Audio/bg_audio/6. Lurking in the Dark.wav")

pygame.mixer.music.set_volume(settings_manager.get_setting("volume"))


def load_game(mission_name, start_menu):
    is_torch_effect = False
    running = True

    def restart_level():
        nonlocal running
        running = False
        load_game(mission_name, start_menu)

    def return_to_main():
        nonlocal running
        game_music.stop()
        start_menu_music.play(-1)
        running = False

    while running:
        level = Level(mission_name, settings_manager)
        clock = pygame.time.Clock()

        pause_menu = PauseMenu("Paused", PAUSE_OPTIONS + ["Quit to Title", "Retry"],
                               level, screen, font, settings_manager, return_to_main, restart_level)
        paused = False

        start_menu_music.stop()
        game_music.play(-1)
        game_music.set_volume(settings_manager.get_setting("volume"))

        if mission_name == "Mission 1":
            level.enemy.enemy_type = "a*"

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused
                    if paused:
                        paused = pause_menu.handle_event(event)

            if paused:
                pause_menu.render()
            else:
                level.run(is_torch_effect)
                pygame.display.flip()
                clock.tick(60)


def main():
    global current_menu
    running = True

    start_menu = Menu("Survival in Shadows", MAIN_OPTIONS + ["Quit Game"], screen, font)
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
                        elif current_menu.selected_option == len(start_menu.options) - 1:  
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
                                "Press SPACE to start the game",
                            ],
                            screen,
                            font,
                            settings_manager
                        )
                        show_start = True
                        while show_start:
                            event2 = pygame.event.wait()
                            show_start = start_screen.handle_event(event2)
                            start_screen.render()

                        load_game(mission_name, start_menu)
                        current_menu = start_menu
                else:
                    current_menu.handle_event(event)

        current_menu.render()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()