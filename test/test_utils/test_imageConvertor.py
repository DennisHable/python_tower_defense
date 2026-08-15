import pygame

from utils.ImageConvertor import ImageConvertor
import constants.Constants as consts

def test_image_convertor():
    # pygame.init()

    assert ImageConvertor.get_name(consts.GAME_PATH) == "game_path"
    assert ImageConvertor.get_name(consts.MAP) == "map"
    assert ImageConvertor.get_name(consts.TOWER) == "tower"
    assert ImageConvertor.get_name(-4) == ""

    assert len(ImageConvertor.resources) == 0

    # assert ImageConvertor.get_img("tower") is not None
    # assert len(ImageConvertor.resources) == 1

    # assert ImageConvertor.get_img("tower") is not None
    # assert len(ImageConvertor.resources) == 1


