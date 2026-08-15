import math

from utils.Position import Position


class Enemy:
    """
    Třída reprezentující nepřítele
    """

    def __init__(self, name: str,
                 health: int,
                 reward: int,
                 speed: int):
        """
        init instančních proměnných
        :param name: jméno nepřítele (označení)
        :param health: aktuální životy nepřitele
        :param reward: odměna za jeho zabití
        :param speed: rychlost pohybu po mapě
        """
        self.__name = name
        self.__health = health
        self.__speed = speed
        self.__reward = reward
        self.__position = None
        self.__move_vector = Position(0, 0)
        self.__enemy_path = None
        self.__act_path_pos = 0

    # gettery

    @property
    def position(self):
        return self.__position

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @property
    def speed(self):
        return self.__speed

    @property
    def reward(self):
        return self.__reward

    @property
    def enemy_path(self):
        return self.__enemy_path

    @property
    def get_move_vector(self):
        return self.__move_vector

    # settery

    @name.setter
    def name(self, value):
        self.__name = value

    @health.setter
    def health(self, value):
        self.__health = value

    @speed.setter
    def speed(self, speed):
        self.__speed = speed

    @reward.setter
    def reward(self, value):
        self.__reward = value

    @position.setter
    def position(self, position):
        self.__position = position

    @enemy_path.setter
    def enemy_path(self, enemy_path):
        self.__enemy_path = enemy_path
        self.__act_path_pos = 0
        self.move_vector()

    def move_vector(self):
        self.__move_vector = self.__enemy_path[self.__act_path_pos] - self.position
        vector_size = math.sqrt(self.__move_vector.x ** 2 + self.__move_vector.y ** 2) # délka vektoru
        # normalizace
        self.__move_vector.x /= vector_size
        self.__move_vector.y /= vector_size

        self.__move_vector.x *= self.speed
        self.__move_vector.y *= self.speed

    def move(self, game_screen_size):
        if self.__act_path_pos < len(self.__enemy_path):
            if math.sqrt((self.__position.x - self.enemy_path[self.__act_path_pos].x) ** 2 + (self.__position.y - self.enemy_path[self.__act_path_pos].y) ** 2) <= self.speed:
                self.__position = self.enemy_path[self.__act_path_pos]
            if self.__position == self.enemy_path[self.__act_path_pos]:
                self.__act_path_pos += 1
                if self.__act_path_pos < len(self.__enemy_path):
                    self.move_vector()

        self.__position += self.__move_vector
        if self.__act_path_pos < len(self.__enemy_path):
            if math.sqrt((self.__position.x - self.enemy_path[self.__act_path_pos].x) ** 2 + (self.__position.y - self.enemy_path[self.__act_path_pos].y) ** 2) <= self.speed:
                self.__position = self.enemy_path[self.__act_path_pos]
        if (self.__position.x > game_screen_size[0] or
                self.__position.x < 0 or
                self.__position.y > game_screen_size[1] or
                self.__position.y < 0):
            return True

        return False


    def get_angle(self):
        return math.degrees(math.atan2(-self.__move_vector.y, self.__move_vector.x))

    def __str__(self):
        return f"Name: {self.__name}, Health: {self.__health}, Reward: {self.__reward}, Speed: {self.__speed}"
