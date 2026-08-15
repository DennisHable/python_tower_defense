import pytest

from entities.GameMap import GameMap
from utils.BfsPathFinder import BfsPathFinder
from utils.Position import Position
import numpy as np

@pytest.mark.parametrize(
    'end_pos, gmap, expected',
    [
        ([Position(3,3)], np.array([[0,0,-1,0],[2,0,0,0],[0,-1,0,3],[0,-1,0,0]]), np.array([[ 6,  5, -1,  5], [-1,  4,  3,  4], [-1, -1,  2, -1], [-1, -1,  1,  0]])),
        ([Position(2,0)], np.array([[0,0,0],[0,0,0],[0,0,0]]), np.array([[2,3,4], [1,2,3], [0,1,2]])),
        ([Position(2,0), Position(2,2)], np.array([[0,0,0],[0,0,0],[0,0,0]]), np.array([[2,3,2], [1,2,1], [0,1,0]])),
        ([Position(2,0), Position(2,2)], np.array([[0,0,0],[0,0,0],[0,0,0]]), np.array([[2,3,2], [1,2,1], [0,1,0]])),
        ([Position(3,7), Position(4,7)], np.array([[0,0,0,1,0,1,0,0], [1,0,1,0,0,0,0,0], [0,0,0,0,0,0,1,0], [0,0,0,0,1,0,0,0], [0,0,1,1,0,0,0,0]]), np.array([[10,9,10,-1,6,-1,4,3], [-1,8,-1,6,5,4,3,2], [8,7,6,5,4,3,-1,1], [9,8,7,6,-1,2,1,0], [10,9,-1,-1,3,2,1,0]])),
        ([Position(1,4), Position(2,4)], np.array([[0,1,0,2,0],[1,0,1,0,0],[0,0,0,3,0]]), np.array([[-1,-1,-1,-1,1], [-1,-1,-1,1,0], [-1,-1,-1,-1,0]]))
    ])
def test_bfs_path_finder(end_pos: list[Position], gmap: np.ndarray, expected: np.ndarray):
    game_map = GameMap(0, 0, [], end_pos, gmap, BfsPathFinder(), [], [])
    dist = BfsPathFinder.find_paths(game_map, end_pos)

    for i in range(game_map.width):
        for j in range(game_map.height):
            assert expected[i][j] == dist[i][j]
