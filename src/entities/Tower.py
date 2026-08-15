import math

import pygame.time

import constants.Constants as consts
from utils.Position import Position


class Tower:
    """
     Třída reprezentuje věž která bude automaticky útočit na nepřátele
    """
    def __init__(self, name: str,
                       attack_damage: int,
                       attack_rate: int,
                       attack_range: int,
                       cost: int):
        """
         kontruktor Tower classy, init instančních proměnných
        :param name: jméno věže
        :param attack_damage: poškození, které věž umí nepříteli způsobit
        :param attack_rate: rychlost útoku věže
        :param attack_range: rozsah útoku věže
        :param cost: cena za věž
        position: umístění věže
        """
        self.__name = name
        self.__attack_damage = attack_damage
        self.__attack_rate = attack_rate
        self.__attack_range = attack_range
        self.__cost = cost
        self.__position = None
        self.__angle = 0
        self.__last_attack = pygame.time.get_ticks()

    @property
    def name(self):
        return self.__name

    @property
    def attack_damage(self):
        return self.__attack_damage

    @property
    def attack_rate(self):
        return self.__attack_rate

    @property
    def attack_range(self):
        return self.__attack_range

    @property
    def cost(self):
        return self.__cost

    @property
    def position(self):
        return self.__position

    @property
    def angle(self):
        return self.__angle

    @name.setter
    def name(self, name: str):
        self.__name = name

    @attack_damage.setter
    def attack_damage(self, attack_damage: int):
        self.__attack_damage = attack_damage

    @attack_rate.setter
    def attack_rate(self, attack_rate: int):
        self.__attack_rate = max(attack_rate, 1)

    @attack_range.setter
    def attack_range(self, attack_range: int):
        self.__attack_range = attack_range

    @position.setter
    def position(self, position):
        self.__position = position

    @angle.setter
    def angle(self, angle):
        self.__angle = angle

    def get_enemy_in_radius(self, act_wave_enemy, navigation_map, tile_size):
        """
         :return: vrací enemy, které je nejblíže k cíly a současně je v rozsahu útoku dané věže
            - do chvíle než může věž opět útočit
        """
        enemy_in_range = None
        for enemy_view in act_wave_enemy:
            enemy = enemy_view.enemy
            tx = self.position.x
            ty = self.position.y
            ex = enemy.position.x
            ey = enemy.position.y


            dist = math.sqrt((ey - ty) ** 2 + (ex - tx) ** 2)
            if dist <= self.__attack_range:
                if enemy_in_range is None:
                    enemy_in_range = enemy_view
                erx = enemy_in_range.enemy.position.x
                ery = enemy_in_range.enemy.position.y
                if navigation_map.get_elem(Position(ex // tile_size[0], ey // tile_size[1])) < navigation_map.get_elem(Position(erx // tile_size[0], ery // tile_size[1])):
                    if enemy_view.enemy.health > 0:
                        enemy_in_range = enemy_view

        return enemy_in_range

    def attack(self, game_map, act_wave_enemy, navigation_map, tile_size):
        success_attack = False
        if pygame.time.get_ticks() - self.__last_attack >= consts.ATTACK_COOLDOWN * self.__attack_rate:
            enemy_view = self.get_enemy_in_radius(act_wave_enemy, navigation_map, tile_size)
            if enemy_view is not None:
                vector = Position(enemy_view.enemy.position.x - self.position.x,
                                  enemy_view.enemy.position.y - self.position.y)
                self.__angle = math.degrees(math.atan2(-vector.y, vector.x))

                enemy_view.enemy.health -= self.attack_damage
                if enemy_view.enemy.health <= 0:
                    game_map.coins += enemy_view.enemy.reward
                    enemy_view.kill()
                success_attack = True
            self.__last_attack = pygame.time.get_ticks()
        return success_attack
