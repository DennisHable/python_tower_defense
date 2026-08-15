from entities.Enemy import Enemy
from entities.EnemyWave import EnemyWave


def test_enemy_wave():
    lst1 = [Enemy("A", 10, 5, 1),
            Enemy("B", 10, 5, 1),
            Enemy("C", 10, 5, 1),
            Enemy("D", 10, 5, 1)]
    enemy_wave = EnemyWave(1, lst1, shuffle = False)

    assert enemy_wave.start_delay == 1

    assert enemy_wave.enemies[0].name == "A"
    assert enemy_wave.enemies[1].name == "B"
    assert enemy_wave.enemies[2].name == "C"
    assert enemy_wave.enemies[3].name == "D"
