import numpy as np
import pytest

import constants.Constants
from entities.NavigationMap import NavigationMap
from utils.BfsPathFinder import BfsPathFinder
from utils.Position import Position


class GameMapTest:
    def __init__(self, map, end_pos):
        self.width = map.shape[0]
        self.height = map.shape[1]
        self.map = map
        self.end_position = end_pos

    def is_walkable(self, pos):
        return self.map[pos.x][pos.y] == constants.Constants.GAME_PATH

@pytest.mark.parametrize(
    'game_map, end_pos, expected',
    [
        (np.array([[1, 1, 0, 1], [0, 0, 0, 0], [0, 1, 1, 0]]), [Position(0, 2)], np.array([[-1, -1, 0, -1], [3, 2, 1, 2], [4, -1, -1, 3]])),
        (np.array([[1, 1, 0, 1], [0, 0, 0, 0], [0, 1, 1, 0]]), [Position(0, 2), Position(2, 3)], np.array([[-1, -1, 0, -1], [3, 2, 1, 1], [4, -1, -1, 0]])),
        (np.array([
              [1,1,1,1,2,1,1,1,1,1],
              [1,2,0,0,0,0,2,1,1,1],
              [2,0,0,0,2,0,0,0,1,1],
              [0,0,1,1,1,1,2,0,0,1],
              [1,1,1,1,1,1,1,1,0,0]
            ]), [Position(4, 9)],
            np.array([
              [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
              [-1,-1,10, 9, 8, 7,-1,-1,-1,-1],
              [-1,12,11,10,-1, 6, 5, 4,-1,-1],
              [14,13,-1,-1,-1,-1,-1, 3, 2,-1],
              [-1,-1,-1,-1,-1,-1,-1,-1, 1, 0]
            ]))
    ]
)
def test_navigation_map(game_map, end_pos, expected):
    nav_map = NavigationMap(GameMapTest(game_map, end_pos), BfsPathFinder())
    for i in range(game_map.shape[0]):
        for j in range(game_map.shape[1]):
            assert nav_map.get_elem(Position(i, j)) == expected[i][j]


@pytest.mark.parametrize(
    'game_map, end_pos, expected',
    [
        (np.array([[1, 1, 0, 1], [0, 0, 0, 0], [0, 1, 1, 0]]), [Position(0, 2)],
         np.array([[-1, -1, 0, -1], [3, 2, 1, 2], [4, -1, -1, 3]])),
        (np.array([[1, 1, 0, 1], [0, 0, 0, 0], [0, 1, 1, 0]]), [Position(0, 2), Position(2, 3)],
         np.array([[-1, -1, 0, -1], [3, 2, 1, 1], [4, -1, -1, 0]])),
    ]
)
def test_navigation_map_get_neighbours(game_map, end_pos, expected):
    nav_map = NavigationMap(GameMapTest(game_map, end_pos), BfsPathFinder())

    res = nav_map.get_neighbours(Position(0, 2))
    assert len(res) == 0

    res = nav_map.get_neighbours(Position(1, 2))
    # [Position(0,1), Position(1,0), Position(-1,0), Position(0,-1)]
    assert len(res) == 1
    assert nav_map.get_elem(res[0]) == expected[0][2]

@pytest.mark.parametrize(
    'game_map, end_pos, expected',
    [
        (np.array([
              [1,1,1,1,2,1,1,1,1,1],
              [1,2,0,0,0,0,2,1,1,1],
              [2,0,0,0,2,0,0,0,1,1],
              [0,0,1,1,1,1,2,0,0,1],
              [1,1,1,1,1,1,1,1,0,0]
            ]), [Position(4, 9)],
            np.array([
              [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
              [-1,-1,10, 9, 8, 7,-1,-1,-1,-1],
              [-1,12,11,10,-1, 6, 5, 4,-1,-1],
              [14,13,-1,-1,-1,-1,-1, 3, 2,-1],
              [-1,-1,-1,-1,-1,-1,-1,-1, 1, 0]
            ]))
    ]
)
def  test_nagivation_map2(game_map, end_pos, expected):
    nav_map = NavigationMap(GameMapTest(game_map, end_pos), BfsPathFinder())

    res = nav_map.get_path(Position(4, 9), (2,2))
    assert res[0].x == 19 and res[0].y == 9 # střed té plochy - pro pohyb enemy ne přímo souřadnice


    nb_elem = nav_map.get_game_path_pos(Position(4, 9))
    assert nb_elem.x == 4 and nb_elem.y == 8

    next_elem = nav_map.get_next(Position(3, 8))
    assert next_elem.x == 4 and next_elem.y == 8

    next_elem = nav_map.get_next(Position(4, 8))
    assert next_elem.x == 4 and next_elem.y == 9