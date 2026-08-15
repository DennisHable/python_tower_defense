from abc import abstractmethod, ABC
import numpy as np

from utils.Position import Position


class PathFinder(ABC):

    # posuny na další pole
    DIRECTIONS = [Position(0,1), Position(1,0), Position(-1,0), Position(0,-1)]

    @staticmethod
    def validate(game_map, pos):
        """ pos.x v 1. dimenzi (max width); pos.y v 2. dimenzi (max height) """
        return 0 <= pos.x < game_map.width and 0 <= pos.y < game_map.height

    @staticmethod
    @abstractmethod
    def find_paths(game_map, start) -> np.ndarray:
        """ Najde cesty ze start v game """
        pass