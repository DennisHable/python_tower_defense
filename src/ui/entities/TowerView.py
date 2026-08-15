import pygame
from pygame.sprite import Sprite

import constants.Constants as consts
from utils.Position import Position


class TowerView(Sprite):
    """
    Zobrazované entity ve hře
    """
    def __init__(self, entity,
                       image,
                       base_img = None):
        Sprite.__init__(self)
        self.__entity = entity
        self.__original_image = image
        self.__base_img = base_img

        orig_img_size = self.__original_image.get_size()
        base_img_size = self.__base_img.get_size()

        self.__image = pygame.Surface(self.__base_img.get_size(), pygame.SRCALPHA)
        self.__image.blit(self.__base_img, (0, 0))
        self.__image.blit(self.__original_image, ((base_img_size[0] - orig_img_size[0]) / 2, (base_img_size[1] - orig_img_size[1]) / 2))

        self.__rect = self.__image.get_rect()
        self.__rect.center = (self.__entity.position.x, self.__entity.position.y)

        self.__is_clicked = False

    @property
    def image(self):
        return self.__image

    @property
    def tower(self):
        return self.__entity

    @property
    def rect(self):
        return self.__rect

    def update(self, game_map, act_wave_enemy, navigation_map, tile_size):
        self.__entity.attack(game_map, act_wave_enemy, navigation_map, tile_size)
        self.rotate()

    def show_range(self, canvas):
        range_surface = pygame.Surface((self.__entity.attack_range * 2, self.__entity.attack_range * 2), pygame.SRCALPHA)
        pygame.draw.circle(range_surface,
                           consts.BTN_TOWER_SELECT_CLR,
                           (self.__entity.attack_range,
                            self.__entity.attack_range),
                           self.__entity.attack_range)
        canvas.blit(
            range_surface,
            (self.__entity.position.x - self.__entity.attack_range,
             self.__entity.position.y - self.__entity.attack_range)
        )


    def event_handler(self, event):
        # aktuální pozice myši
        pos = pygame.mouse.get_pos()

        clicked = False

        # konrola kolize myši a veže a reakce na kliknutí
        if self.__rect.collidepoint(pos): # kolize věže a myší
            if (event.type == pygame.MOUSEBUTTONDOWN and # kliknutí tlačítkem myši
                    event.button == 1  # stisknuto levé tlačítko
                    and self.__is_clicked == False): # pokud už není tlačítko stisknuto
                clicked = True # došlo ke stisknutí tlačítka
                self.__is_clicked = True # tahle proměnná tady je protože jinak by to provedlo na jeden klik více klinutí

        if pygame.mouse.get_pressed()[0] == 0: # když je tlačítko uvolněno
            self.__is_clicked = False # označí, že už není stisknuté

        return clicked

    def rotate(self):
        """
            rotace obrázku na základě "zaměřeného" enemy
        """
        angle = self.__entity.angle
        rect = self.__image.get_rect(center=(self.__entity.position.x, self.__entity.position.y))

        self.__image = pygame.Surface(self.__base_img.get_size(), pygame.SRCALPHA)
        self.__image.blit(self.__base_img, (0, 0))

        base_img_size = self.__base_img.get_size()

        rotated_tower_img = pygame.transform.rotate(self.__original_image, angle - 90)
        rotated_tower_img_size = rotated_tower_img.get_size()
        self.__image.blit(rotated_tower_img,
                          ((base_img_size[0] - rotated_tower_img_size[0]) / 2,
                           (base_img_size[1] - rotated_tower_img_size[1]) / 2))

        self.__rect = self.__image.get_rect()
        self.__rect.center = rect.center