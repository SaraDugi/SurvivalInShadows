WIDTH = 1080
HEIGHT = 700
FPS = 60

MAX_STEPS =  100

TILESIZE = 48

BAR_HEIGHT = 00
HEALTH_BAR_WIDTH = 000
ENERGY_BAR_WIDTH = 00

UI_FONT = '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18
LIGHT_RADIUS = 192

PLAYER_START_POS = (2448, 816)
ENEMY_START_POS = (1872, 816)

WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#000000'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT_SIZE = 55
GREEN = (0, 255, 0)
RED = (255, 0, 0)

STAMINA_REDUCTION = 10  
STAMINA_COOLDOWN = 1000  
SPEED_BOOST_DURATION = 5000

MAIN_OPTIONS = ['Start Game', 'Exit Game']
MISSION_OPTIONS = ['Mission 1', 'Mission 2', 'Mission 3', 'Mission 4', 'Mission 5']
PAUSE_OPTIONS = ['Resume', 'Quit to start menu', 'Quit the game']

monster_data =  {
    '1': {'speed':3, 'damage': 100, 'chase_radius': 5000, 'notice_radius': 100}
}