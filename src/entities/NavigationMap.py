from utils.PathFinder import PathFinder
from utils.Position import Position
import constants.Constants as consts

class NavigationMap:
    def __init__(self, game_map, path_finder: PathFinder):
        self.__game_map = game_map
        self.__dist= path_finder.find_paths(game_map, game_map.end_position)

    def get_elem(self, pos) -> int:
        pos.x = int(pos.x)
        pos.y = int(pos.y)
        if (0 <= pos.x < self.__dist.shape[0] and
                0 <= pos.y < self.__dist.shape[1]):
            return self.__dist[pos.x][pos.y]
        return -1

    def get_neighbours(self, pos):
        res = []
        pos.x = int(pos.x)
        pos.y = int(pos.y)
        for direction in PathFinder.DIRECTIONS:
            act_pos = pos + direction
            if (PathFinder.validate(self.__game_map, act_pos) and
                    self.get_elem(pos) > self.get_elem(act_pos) != -1):
                res.append(act_pos)
        return res

    def get_game_path_pos(self, pos):
        res = None
        pos.x = int(pos.x)
        pos.y = int(pos.y)
        for direction in PathFinder.DIRECTIONS:
            act_pos = pos + direction
            if (PathFinder.validate(self.__game_map, act_pos) and
                    self.get_elem(act_pos) != -1):
                res = act_pos
        return res

    def get_next(self, pos):
        nbs = self.get_neighbours(pos)
        pos = nbs[0]
        for act in nbs:
            if self.get_elem(act) < self.get_elem(pos):
                pos = act
        return pos

    def get_path(self, start_pos, tile_size):
        res = []

        while self.get_elem(start_pos) != 0:
            res.append(Position(start_pos.y * tile_size[0] + tile_size[0] / 2,
                                start_pos.x * tile_size[1] + tile_size[1] / 2))
            start_pos = self.get_next(start_pos)

        res.append(Position(start_pos.y * tile_size[0] + tile_size[0] / 2,
                            start_pos.x * tile_size[1] + tile_size[1] / 2))
        return res