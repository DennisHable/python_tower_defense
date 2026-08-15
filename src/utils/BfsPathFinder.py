import numpy as np

from utils.PathFinder import PathFinder
from utils.Position import Position


class BfsPathFinder(PathFinder):
    @staticmethod
    def find_paths(game_map, start: list[Position]) -> np.ndarray:
        queue = []
        # prev = {}
        dist = np.full((game_map.width, game_map.height), fill_value=-1, dtype=int)
        for pos in start:
            queue.append(pos)
            dist[pos.x][pos.y] = 0
            # prev[pos] = Position(-1, -1)

        while queue.__len__() > 0:
            act_pos = queue.pop(0)

            for direction in PathFinder.DIRECTIONS:
                next_pos = act_pos + direction
                if (PathFinder.validate(game_map, next_pos) and
                        dist[next_pos.x][next_pos.y] == -1 and
                        game_map.is_walkable(next_pos)):
                    queue.append(next_pos)
                    dist[next_pos.x][next_pos.y] = dist[act_pos.x][act_pos.y] + 1
                    # prev[next_pos] = act_pos

        # path = []
        # act = end
        # while act != prev[start]:
        #    path.append(act)
        #    act = prev[act]

        return dist
