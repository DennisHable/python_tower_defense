import os

import pygame
import constants.Constants as consts
from ui.GameView import GameView
from ui.LevelView import LevelView
from ui.MainView import MainView
from utils.BfsPathFinder import BfsPathFinder
from utils.JsonMapLoader import JsonMapLoader


class Game:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()

        self.__img = pygame.image.load(consts.WINDOW_ICON)  # ikona appky
        pygame.display.set_icon(self.__img)  # nastavení icony

        pygame.display.set_caption(consts.WINDOW_NAME)  # název okna

        self.__clock = pygame.time.Clock()
        self.__running = True
        self.__current_screen = None
        self.__canvas = None

        self.__act_level = -1

        # startovní obrazovka
        self.change_screen(MainView())

    def change_screen(self, screen):
        """
        Přepne obrazovku a případně změní velikost okna.
        """
        # smaže aktuální obrazovku
        # zjisti požadovanou velikost obrazovky a změní velikost okna
        # if self.__canvas is None:
        self.__canvas = pygame.display.set_mode(
    screen.window_size,
     pygame.SCALED | pygame.DOUBLEBUF
)
        self.__current_screen = screen

    def run(self):
        """
         hlavní herni smyčka
        """
        while self.__running:
            self.__clock.tick(consts.FPS) # rychlost renderování hry

            self.__canvas.fill((100, 100, 100)) # vyplní celou obrazovku barvou

            if self.__current_screen is not None:
                self.__current_screen.draw(self.__canvas)

            # obsluha událostí
            for event in pygame.event.get():
                # ukončí program
                if event.type == pygame.QUIT:
                    self.__running = False

                if self.__current_screen is not None:
                    ret_code = self.__current_screen.event_handler(event)
                    # reakce na kliknutí na tlačítko z hlavního menu
                    if ret_code == consts.END:  # konec hry
                        self.__running = False
                    elif ret_code == consts.RUN_GAME :  # vykreslení herní obrazovky
                        self.change_screen(LevelView())
                    elif ret_code == consts.BACK:
                        self.change_screen(MainView())
                        self.__act_level = -1
                    elif ret_code == consts.LEVEL_SELECTED or ret_code == consts.PLAY_AGAIN:
                        if self.__act_level == -1:
                            self.__act_level = self.__current_screen.level
                        self.change_screen(GameView(JsonMapLoader.load(consts.get_lvl(self.__act_level),
                                                                       consts.PATH_FINDER),
                                                    consts.GAME_SCREEN_SIZE,
                                                    consts.SCREEN_SIZE))


            # aktualizace obrazovky (změn)
            pygame.display.flip()

        pygame.quit()


