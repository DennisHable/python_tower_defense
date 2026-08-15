import random

from entities.Enemy import Enemy


class EnemyWave:
    def __init__(self, start_delay: int,
                       enemies: list[Enemy],
                       shuffle = True):
        self.__start_delay = start_delay
        self.__enemies = enemies
        if shuffle:
            random.shuffle(self.__enemies)

    @property
    def start_delay(self):
        return self.__start_delay

    @property
    def enemies(self):
        return self.__enemies
