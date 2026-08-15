import pygame

from ui.Button import Button
import constants.Constants as consts

class LevelView:
    def __init__(self):
        self.__image = pygame.image.load(consts.MAIN_IMG)  # obrázek na pozadí úvodního okna

        [w, h] = self.__image.get_size()  # rozměry pozadí okna budou stejné jako rozměry obrázku

        self.__window_size = (w, h)
        self.level = -1
        self.__lvls = []
        pos_height = h // 4
        for i in range(consts.LVL_CNT):
            self.__lvls.append((i + 1, Button((w // 2, pos_height),
                               (consts.BTN_LVL_WIDTH, consts.BTN_LVL_HEIGHT),
                               consts.BTN_BG_COLOR, text=f"Level {i + 1}",
                               font_size=consts.TEXT_FONT_SIZE)))
            pos_height += consts.BTN_LVL_HEIGHT + 5

        self.__back_to_menu = Button((w // 2, pos_height + 10),
                               (consts.BTN_LVL_WIDTH, consts.BTN_LVL_HEIGHT),
                               consts.BTN_BG_COLOR, text="Back to menu",
                                     font_size=consts.TEXT_FONT_SIZE + 5)

    @property
    def window_size(self):
        return self.__window_size

    def draw(self, canvas):
        canvas.blit(self.__image, (0, 0))
        for btn in self.__lvls:
            btn[1].draw(canvas)
        self.__back_to_menu.draw(canvas)

    def event_handler(self, event):
        for btn in self.__lvls:
            if btn[1].event_handler(event):
                self.level = btn[0]
                return consts.LEVEL_SELECTED
        if self.__back_to_menu.event_handler(event):
            return consts.BACK
        return consts.OK