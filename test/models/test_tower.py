from entities.Tower import Tower


def test_tower():
    tower = Tower("test_tower", 100, 50, 20, 30)
    assert (tower.name == "test_tower" and
            tower.attack_damage == 100 and
            tower.attack_rate == 50 and
            tower.attack_range == 20 and
            tower.cost == 30)

    tower.name = "test"
    assert tower.name == "test"

    tower.attack_damage = 200
    assert tower.attack_damage == 200

    tower.attack_rate = 789
    assert tower.attack_rate == 789

    tower.attack_range = 428
    assert tower.attack_range == 428



