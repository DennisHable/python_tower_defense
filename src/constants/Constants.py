import glob
from utils.BfsPathFinder import BfsPathFinder

"""
 Konstanty a konfigurační soubor pro celou hru - 
    ovlivňuje chování nepřátel, rychlost renderování, načítání textur, vykreslování, ...
"""

# konfigurační soubory, levely, assety pro celou hru
RESOURCES = "resources/"

# ikona aplikace
WINDOW_ICON = RESOURCES + "PNG/Default size/towerDefense_tile206.png"
# pozadí na hlavní menu
MAIN_IMG = RESOURCES + "Example.png"
# název hry
WINDOW_NAME = "Tower Defence"

FPS = 60 # rychlost renderování hry (snímky za vteřinu)

# složka s levely pro hru
LVL_DIR = RESOURCES + "Game/levels/"


prefix = "lvl"
suffix = ".json"
pattern = f"{LVL_DIR}{prefix}*{suffix}"

LVL_CNT = len(glob.glob(pattern)) # počet levelů ve složce LVL_DIR

# vrací název souboru s levelem (určeno pomocí idx)
def get_lvl(idx):
    return LVL_DIR + f"lvl{idx}.json"

# konfigurační soubor - určuje které assety se použijí pro různé věže/nepřátele/cestu/....
ICONS = RESOURCES + "Game/icons.json"

# složka s texturama
ASSETS_DIR = RESOURCES + "/PNG/Default size/"


# konstanty pro tlačítka
BTN_COLOR = (0, 0, 0)
BTN_FONT_NAME = None
BTN_WIDTH = 250
BTN_HEIGHT = 80
BTN_BG_COLOR = (100, 100, 100)
BTN_BG_COLOR2 = (6, 112, 225)
BTN_BG_COLOR_ACTIVE = (180, 180, 180)
BTN_BG_COLOR_CLICKED = (240, 240, 240)
BTN_FONT_SIZE = 80


BTN_TOWER_SELECT_CLR = (200, 200, 200, 100) # rgb průhlednost

# eventy po kliknutí na tlačítko - kvůli oddělení view a controlleru (snad)
OK = 0
END = 1
RUN_GAME = 2
PLAY_AGAIN = 3
BACK = 4
LEVEL_SELECTED = 5

# velikost okna - hry, obrazovky, menu
GAME_SCREEN_SIZE = (800, 600)
PANEL_SIZE = 360
SCREEN_SIZE = (GAME_SCREEN_SIZE[0] + PANEL_SIZE, GAME_SCREEN_SIZE[1])

# určuje který algoritmus se použíje pro hledání cesty ze startu do cíle
PATH_FINDER = BfsPathFinder()

# hodnoty z mapy levlů
GAME_PATH = 0
MAP = 1
TOWER = 2

#rychlost spawnování nepřátel za sebou v jedné vlně
SPAWN_COOLDOWN = 700

# počet životů na level
GAME_LIVES = 20

# text - fonty, velikost, barva
TEXT_FONT_NAME = None
TEXT_FONT_SIZE = 40
TEXT_FONT_SIZE_DESCRIPTION = 26
TEXT_COLOR = (0,0,0)

# velikost náhledu veží v tower menu
TOWER_VIEW_WIDTH = 50
TOWER_VIEW_HEIGHT = 50

# od jaké pozice (y) se bude renderovat nabídka věží
TOWER_MENU_HEIGHT_POS = 200

# rozdíl mezi velikostí věže a základny pro věž
BASE_TOWER_DIFF = 15

# základní rychlost útoku věží
ATTACK_COOLDOWN = 500

# velikost upgrade buttons
BTN_UPG_WIDTH = 250
BTN_UPG_HEIGHT = 50

BTN_UPG_FONT_SIZE = 30

# cena upgrade
UPGRADE_COST = 10

# hodnota upgrade
UPGRADE_VAL = 2

# velikost ovládacích tlačítek
BTN_CTRL_WIDTH = 150
BTN_CTRL_HEIGHT = 50

# velikosti tlačítek pro levely
BTN_LVL_WIDTH = 300
BTN_LVL_HEIGHT = 40