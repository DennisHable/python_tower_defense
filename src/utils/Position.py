""" Reprezentuje 2D souřadnice """
class Position:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @x.setter
    def x(self, value):
        self.__x = value

    @y.setter
    def y(self, value):
        self.__y = value

    def __add__(self, other):
        return Position(self.__x + other.x, self.__y + other.y)

    def __sub__(self, other):
        return Position(self.__x - other.x, self.__y - other.y)

    def __eq__(self, other):
        return self.__x == other.x and self.__y == other.y