import pygame
import constants.Constants as consts
from entities.GameMap import GameMap
from ui.Button import Button


class MainView:
    def __init__(self):
        self.__image = pygame.image.load(consts.MAIN_IMG)  # obrázek na pozadí úvodního okna

        [w, h] = self.__image.get_size()  # rozměry pozadí okna budou stejné jako rozměry obrázku

        self.__window_size = (w, h)

        self.__start_button = Button((w // 2, h // 2), (consts.BTN_WIDTH, consts.BTN_HEIGHT), consts.BTN_BG_COLOR, text="Play")
        self.__settings_button = None
        self.__stats_button = None
        self.__end_button =  Button((w // 2, h // 2 + consts.BTN_HEIGHT + 10), (consts.BTN_WIDTH, consts.BTN_HEIGHT), consts.BTN_BG_COLOR, text="End")

    @property
    def window_size(self):
        return self.__window_size

    def event_handler(self, event):
        if self.__start_button.event_handler(event):
            return consts.RUN_GAME
        if self.__end_button.event_handler(event):
            return consts.END
        return consts.OK

    def draw(self, canvas):
        canvas.blit(self.__image, (0, 0))
        self.__start_button.draw(canvas)
        self.__end_button.draw(canvas)

