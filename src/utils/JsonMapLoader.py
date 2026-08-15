import json
import numpy as np

from entities.Enemy import Enemy
from entities.EnemyWave import EnemyWave
from entities.GameMap import GameMap
from entities.Tower import Tower
from utils.PathFinder import PathFinder
from utils.Position import Position


class JsonMapLoader:
    @staticmethod
    def load(file_name: str, path_finder: PathFinder, shuffle = True) -> GameMap:
        with open(file_name, 'r') as file:
            data = json.load(file)

        info = data["info"]
        gmap = data["map"]

        start_position = []
        for rec in gmap["start_positions"]:
            start_position.append(Position(rec["x"], rec["y"]))

        end_position = []
        for rec in gmap["end_positions"]:
            end_position.append(Position(rec["x"], rec["y"]))

        towers = []
        for tower in data["towers"]:
            towers.append(Tower(tower["type_name"],
                                tower["attack_damage"],
                                tower["attack_rate"],
                                tower["attack_range"],
                                tower["cost"]))

        # enemies = []
        enemies_map = dict()
        for enemy in data["enemies"]:
            act_enemy = Enemy(enemy["type"],
                              enemy["hp"],
                              enemy["reward"],
                              enemy["speed"])
            enemies_map[enemy["type"]] = act_enemy
            # enemies.append(act_enemy)

        waves = []
        for wave_info in data["waves"]:
            start_delay = wave_info["start_delay"]
            wave_enemies = []
            for enemy in wave_info["enemies"]:
                type_name = enemy["type"]
                enemy_entity = enemies_map[type_name]
                for i in range(enemy["count"]):
                    wave_enemies.append(Enemy(type_name,
                                              enemy_entity.health,
                                              enemy_entity.reward,
                                              enemy_entity.speed))
            waves.append(EnemyWave(start_delay, wave_enemies, shuffle = shuffle))

        return GameMap(info["level_id"],
                       info["initial_coins"],
                       start_position,
                       end_position,
                       np.array(gmap["game_map"]),
                       path_finder,
                       towers,
                       waves)
