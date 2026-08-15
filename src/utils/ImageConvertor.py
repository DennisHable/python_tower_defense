import json

import pygame.image

import constants.Constants as consts


class ImageConvertor:
    resources = dict()
    loaded = False

    @classmethod
    def __load(cls):
        with open(consts.ICONS, 'r') as file:
            data = json.load(file)

        for d in data:
            cls.resources[d] = pygame.image.load(consts.ASSETS_DIR + data[d]).convert_alpha()

    @classmethod
    def get_name(cls, num):
        if num == consts.GAME_PATH:
            return "game_path"
        if num == consts.MAP:
            return "map"
        if num == consts.TOWER:
            return "tower"
        return ""

    @classmethod
    def get_img(cls, name, size = None):
        if not cls.loaded:
            cls.__load()
            cls.loaded = True
        if name in cls.resources:
            if size is not None:
                cls.resources[name] = pygame.transform.scale(cls.resources[name], size)
            return cls.resources[name]
        return None

