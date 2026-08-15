import numpy as np
import pytest

import constants.Constants as consts
from utils.BfsPathFinder import BfsPathFinder
from utils.JsonMapLoader import JsonMapLoader

def test_json_map_loader():
    expected_map = np.array([
      [1,1,1,1,2,1,1,1,1,1],
      [1,2,1,0,0,0,2,1,1,1],
      [2,0,0,0,2,0,0,0,1,1],
      [0,0,1,1,1,1,2,0,0,1],
      [1,1,1,1,1,1,1,1,0,0]
    ])
    game_map = JsonMapLoader.load(consts.RESOURCES + "Game/test_lvl.json",
                                  BfsPathFinder(),
                                  shuffle = False)
    assert game_map is not None
    assert game_map.coins == 40
    for i in range(expected_map.shape[0]):
        for j in range(expected_map.shape[1]):
            assert game_map.game_map[i][j] == expected_map[i][j]
    assert game_map.start_positions[0].x == 3 and game_map.start_positions[0].y == 0
    assert game_map.end_positions[0].x == 4 and game_map.end_positions[0].y == 9
    available_towers = game_map.available_towers
    assert (available_towers[0].name == "gun_lvl1" and
            available_towers[0].attack_damage == 5 and
            available_towers[0].attack_rate == 1 and
            available_towers[0].attack_range == 200 and
            available_towers[0].cost == 10)
    assert (available_towers[1].name == "rocket_tower" and
            available_towers[1].attack_damage == 10 and
            available_towers[1].attack_rate == 2 and
            available_towers[1].attack_range == 180 and
            available_towers[1].cost == 20)

    enemies = game_map.enemies[0].enemies
    assert len(enemies) == 5
    assert (enemies[0].name == "basic" and
            enemies[0].health == 15 and
            enemies[0].reward == 1 and
            enemies[0].speed == 1 )

    enemies = game_map.enemies[1].enemies
    print(enemies)

    assert len(enemies) == 8
    assert (enemies[0].name == "basic" and
            enemies[0].health == 15 and
            enemies[0].reward == 1 and
            enemies[0].speed == 1 )
    assert (enemies[5].name == "fast" and
            enemies[5].health == 10 and
            enemies[5].reward == 2 and
            enemies[5].speed == 2 )

    enemies = game_map.enemies[2].enemies
    assert len(enemies) == 8
    assert (enemies[0].name == "tank_1" and
            enemies[0].health == 25 and
            enemies[0].reward == 10 and
            enemies[0].speed == 1 )
    assert (enemies[2].name == "fast" and
            enemies[2].health == 10 and
            enemies[2].reward == 2 and
            enemies[2].speed == 2 )

    enemies = game_map.enemies[3].enemies
    assert len(enemies) == 18
    assert (enemies[0].name == "basic" and
            enemies[0].health == 15 and
            enemies[0].reward == 1 and
            enemies[0].speed == 1 )
    assert (enemies[10].name == "tank_1" and
            enemies[10].health == 25 and
            enemies[10].reward == 10 and
            enemies[10].speed == 1 )
    assert (enemies[12].name == "fast" and
            enemies[12].health == 10 and
            enemies[12].reward == 2 and
            enemies[12].speed == 2 )