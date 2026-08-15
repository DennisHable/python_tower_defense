import pygame
from pygame.sprite import Sprite

from utils.Position import Position


class EnemyView(Sprite):
    """
    Zobrazované entity ve hře
    """
    def __init__(self, entity,
                       image):
        Sprite.__init__(self)
        self.__entity = entity
        self.__original_image = image
        self.__image = image
        self.__rect = self.__image.get_rect()
        self.__rect.center = (self.__entity.position.x, self.__entity.position.y)

    @property
    def image(self):
        return self.__image

    @property
    def enemy(self):
        return self.__entity

    @property
    def rect(self):
        return self.__rect

    def update(self, game, game_screen_size):
        self.rotate()
        if self.__entity.move(game_screen_size): # pohyb po hrací ploše; true -> je mimo mapu = došel do cíle
            if self.__entity.health > 0: # pokud ho nějaká věž ještě na úplném konci před odečtením bodu nezabila
                self.kill() # destrukce enemy
                self.__entity.health = 0
                game.lives -= 1 # odečtení života
        else:
            self.__rect.center = (self.__entity.position.x, self.__entity.position.y) # aktualizace pozice enemy - obrázku

    def rotate(self):
        """
            rotace obrázku na základě směru vektoru pohybu enemy
        """
        angle = self.__entity.get_angle()
        rect = self.__image.get_rect(center=(self.__entity.position.x, self.__entity.position.y))
        self.__image = pygame.transform.rotate(self.__original_image, angle)
        self.__rect = self.__image.get_rect()
        self.__rect.center = rect.center