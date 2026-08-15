import math
from platform import android_ver

from entities.Enemy import Enemy
from utils.Position import Position


def test_enemy():
    enemy = Enemy("test_enemy", 123, 11, 20)
    assert (enemy.name == "test_enemy" and
            enemy.health == 123 and
            enemy.reward == 11 and
            enemy.speed == 20)
    enemy.name = "test"
    assert enemy.name == "test"
    enemy.health = 1
    assert enemy.health == 1
    enemy.reward = 23
    assert enemy.reward == 23
    enemy.speed = 101
    assert enemy.speed == 101

    enemy.speed = 2
    assert enemy.speed == 2

    enemy.position = Position(0, 0)
    enemy.enemy_path = [Position(1, 0), Position(1, 1), Position(0, 1)]

    assert enemy.enemy_path[0].x == 1
    assert enemy.enemy_path[0].y == 0

    assert enemy.enemy_path[1].x == 1
    assert enemy.enemy_path[1].y == 1

    assert enemy.enemy_path[2].x == 0
    assert enemy.enemy_path[2].y == 1

    assert enemy.position.x == 0 and enemy.position.y == 0

    move_vector = enemy.get_move_vector
    assert move_vector.x == 2
    assert move_vector.y == 0

    assert not enemy.move((200, 100))

    move_vector = enemy.get_move_vector
    assert move_vector.x == 0
    assert move_vector.y == 2

    assert enemy.position.x == 1
    assert enemy.position.y == 1

    assert enemy.get_angle() == -90



