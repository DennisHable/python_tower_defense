import pygame
from pygame.sprite import Sprite
from pygame import font
import constants.Constants as consts

class Button(Sprite):
    """
    Třída reprezentující tlačítko
    """
    def __init__(self, position, size, bg_color = None, image = None, text = None, pos_mid = True, font_size = consts.BTN_FONT_SIZE):
        """
        :param position: umístění tlačítka - střed (pod_mid = True) jinak levý horní roh
        :param image: obrázek co se zobrazí; pokud není None
        :param text: text co se zobrazí; pokud není None
        """
        Sprite.__init__(self)
        self.__is_clicked = False # tlačítko bylo stisknuto
        self.__is_selected = False # je na něm myš
        self.__size = size
        self.__bg_color = bg_color
        self.__bg_color_orig = bg_color
        self.__pos_mid = pos_mid

        self.__text = None
        self.__image = image
        self.__position = position

        # pokud je nastaven text tak se z něj udělá obrázek a ten se zobrazí na tlačítko
        if text is not None:
            # vytvoření obrázku z textu
            self.__text = (font.SysFont(consts.BTN_FONT_NAME, font_size)
                           .render(text, True, consts.BTN_COLOR))

            self.__image = pygame.Surface(self.__size) # oblast/podklad o velikosti size
            self.__image.fill(self.__bg_color) # vyplní to barvou

            # vykreslí text doprostřed té plochy
            self.__image.blit(self.__text, self.__text.get_rect(center=(self.__size[0] // 2, self.__size[1] // 2)))

        self.__rect = self.__image.get_rect() # obdélník okolo obrázku
        if pos_mid:
            self.__rect.center = position # pozice tlačítka
        else:
            self.__rect.topleft =  position
        # raise Exception("Invalid args: image and text are both None")

    @property
    def position(self):
        return self.__position

    @property
    def size(self):
        return self.__size

    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect

    # def update(self, canvas, event):
    #    return self.event_handler(event)

    def event_handler(self, event):
        # aktuální pozice myši
        pos = pygame.mouse.get_pos()

        clicked = False

        # konrola kolize myši a tlačítka a reakce na kliknutí
        if self.__rect.collidepoint(pos): # kolize tlačítka a myší
            self.__bg_color = consts.BTN_BG_COLOR_ACTIVE
            self.__is_selected = True
            if (event.type == pygame.MOUSEBUTTONDOWN and # kliknutí tlačítkem myši
                    event.button == 1 # stisknuto levé tlačítko
                    and self.__is_clicked == False): # pokud už není tlačítko stisknuto
                self.__bg_color = consts.BTN_BG_COLOR_CLICKED
                clicked = True # došlo ke stisknutí tlačítka
                self.__is_clicked = True # tahle proměnná tady je protože jinak by to provedlo na jeden klik více klinutí
        else:
            self.__bg_color = self.__bg_color_orig
            self.__is_selected = False

        if pygame.mouse.get_pressed()[0] == 0: # když je tlačítko uvolněno
            self.__is_clicked = False # označí, že už není stisknuté

        return clicked

    def draw(self, canvas):
        if self.__text is not None:
            # plocha pro tlačítko o velikosti size
            self.__image = pygame.Surface(self.__size)
            self.__image.fill(self.__bg_color)

            # vykreslí text doprostřed té plochy
            self.__image.blit(self.__text, self.__text.get_rect(center=(self.__size[0] // 2, self.__size[1] // 2)))
            self.__rect = self.__image.get_rect()
            if self.__pos_mid:
                self.__rect.center = self.__position  # pozice tlačítka
            else:
                self.__rect.topleft = self.__position

        #vykreslí tlačítko na canvas
        canvas.blit(self.__image, self.__rect)

        if self.__text is None and self.__is_selected: # pro obrázky se tam vykreslí částečně průhledný obdélník
            rect_surface = pygame.Surface(self.__size, pygame.SRCALPHA)
            rect_surface.fill(consts.BTN_TOWER_SELECT_CLR)
            canvas.blit(rect_surface, self.__rect)
