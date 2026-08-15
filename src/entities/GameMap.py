import random

import numpy as np
from pygame.sprite import Group
from entities.EnemyWave import EnemyWave
from entities.NavigationMap import NavigationMap
from entities.Tower import Tower
from utils.PathFinder import PathFinder
from utils.Position import Position
import constants.Constants as consts

class GameMap:
    def __init__(self, level_id: int,
                       initial_coins: int,
                       start_positions: list[Position],
                       end_positions: list[Position],
                       game_map: np.ndarray,
                       path_finder: PathFinder,
                       available_towers: list[Tower],
                       enemy_waves: list[EnemyWave]):

        self.__width = game_map.shape[0]
        self.__height = game_map.shape[1]

        self.__level_id = level_id
        self.__coins = initial_coins
        self.__lives = consts.GAME_LIVES
        self.__start_positions = start_positions
        self.__end_positions = end_positions
        self.__game_map = game_map
        self.__path_finder = path_finder
        self.__available_towers = available_towers

        self.__enemy_waves_idx = 0
        self.__enemy_in_act_wave_idx = 0
        self.__enemy_waves = enemy_waves

        self.__navigation_map = NavigationMap(self, self.__path_finder)


    def get_elem(self, pos: tuple[int, int]):
        return self.__game_map[pos[0]][pos[1]]

    @property
    def width(self):
        return self.__width

    @property
    def start_positions(self):
        return self.__start_positions

    @property
    def end_positions(self):
        return self.__end_positions

    @property
    def game_map(self):
        return self.__game_map

    @property
    def enemies(self):
        return self.__enemy_waves

    @property
    def coins(self):
        return self.__coins

    @property
    def available_towers(self):
        return self.__available_towers

    @property
    def height(self):
        return self.__height

    @property
    def start_position(self):
        return self.__start_positions

    @property
    def end_position(self):
        return self.__end_positions

    @property
    def navigation_map(self):
        return self.__navigation_map

    @coins.setter
    def coins(self, coins):
        self.__coins = coins

    def is_walkable(self, pos):
        return self.__game_map[pos.x][pos.y] == consts.GAME_PATH

    def next_wave(self):
        self.__enemy_in_act_wave_idx = 0
        self.__enemy_waves_idx += 1

    def waves_done(self):
        return self.__enemy_waves_idx >= len(self.__enemy_waves)


    def wave(self, tile_size):
        if (self.__enemy_waves_idx >= len(self.__enemy_waves) or
                self.__enemy_in_act_wave_idx >= len(self.__enemy_waves[self.__enemy_waves_idx].enemies)):
            return None
        enemy = self.__enemy_waves[self.__enemy_waves_idx].enemies[self.__enemy_in_act_wave_idx]
        idx = random.randint(0, len(self.start_position) - 1)

        enemy.position = Position(tile_size[0] * self.start_position[idx].y, tile_size[1] * self.start_position[idx].x)

        pos = Position(self.start_position[idx].x, self.start_position[idx].y)

        nb = self.__navigation_map.get_next(pos)

        if pos.x == nb.x:
            enemy.position.y += tile_size[1] / 2

        if pos.y == nb.y:
            enemy.position.x += tile_size[0] / 2
            enemy.position.y += tile_size[1]


        enemy.enemy_path = self.__navigation_map.get_path(pos, tile_size)

        self.__enemy_in_act_wave_idx += 1
        return enemy

    @property
    def lives(self):
        return self.__lives

    @lives.setter
    def lives(self, lives):
        self.__lives = lives