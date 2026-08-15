import math

import pygame.time
from pygame.examples.music_drop_fade import draw_text_line

from entities.Tower import Tower
from ui.Button import Button
from ui.entities.EnemyView import EnemyView
from ui.entities.TowerView import TowerView
from utils.ImageConvertor import ImageConvertor
from pygame.sprite import Group
import constants.Constants as consts
from utils.Position import Position


class GameView:
    def __init__(self, game_map, game_screen_size, screen_size):
        self.__game_map = game_map
        self.__game_screen_size = game_screen_size
        self.__screen_size = screen_size
        self.__towers_group = [] # tlačítka pro pokládání věží
        self.__done = False # aby se s každým volání draw nevytvářely nový tlačítka
        self.__act_wave = Group() # enemy v aktuální vlně
        self.__placed_towers = Group() # koupené věže
        self.__start = True
        self.__wave_done = False
        self.__player_is_ready = False
        self.__start_btn = Button((self.__game_screen_size[0] + 30, self.__game_screen_size[1] - 10 - consts.BTN_CTRL_HEIGHT),
                        (consts.BTN_UPG_WIDTH, consts.BTN_UPG_HEIGHT),
                           bg_color=consts.BTN_BG_COLOR2,
                           font_size = consts.BTN_UPG_FONT_SIZE,
                           text = "Start Game",
                           pos_mid = False)
        self.__last_spawn = pygame.time.get_ticks() # pro postupné vytváření nepřátel
        self.__is_towers_menu_visible = False
        self.__tower_menu_btns = self.__create_towers_menu()
        self.__tower_upgrade_btns = self.__create_upgrade_view()
        self.__game_over = self.__create_game_over_view()
        self.__clicked_button = None
        self.__active_placed_tower = None

    @property
    def window_size(self):
        return self.__screen_size

    def draw(self, canvas):
        self.update()
        w = self.__game_map.width
        h = self.__game_map.height
        tile_w = round(self.__game_screen_size[0] / h)
        tile_h = round(self.__game_screen_size[1] / w)
        for i in range(w):
            for j in range(h):
                elem = self.__game_map.get_elem((i, j))
                img = ImageConvertor.get_img(ImageConvertor.get_name(elem), (tile_w, tile_h))
                if elem == consts.TOWER and not self.__done:
                    self.__towers_group.append(Button((tile_w * j, tile_h * i),
                                                      (tile_w, tile_h),
                                                      consts.BTN_BG_COLOR,
                                                      image=img,
                                                      pos_mid=False))
                else:
                    canvas.blit(img, (tile_w * j, tile_h * i))
                j += 1
            i += 1

        self.__done = True

        for tower in self.__towers_group:
            tower.draw(canvas)

        self.__act_wave.draw(canvas)
        self.__placed_towers.draw(canvas)

        lives_img = (pygame.font.SysFont(consts.TEXT_FONT_NAME, consts.TEXT_FONT_SIZE)
                       .render("Lives: " + str(self.__game_map.lives), True, consts.TEXT_COLOR))

        canvas.blit(lives_img, (self.__game_screen_size[0] + 20, 20))

        coins_img = (pygame.font.SysFont(consts.TEXT_FONT_NAME, consts.TEXT_FONT_SIZE)
                       .render("Coins: " + str(self.__game_map.coins), True, consts.TEXT_COLOR))

        canvas.blit(coins_img, (self.__game_screen_size[0] + 20, 20 + consts.TEXT_FONT_SIZE))


        if self.__active_placed_tower is not None:
            self.__active_placed_tower.show_range(canvas)


        self.draw_towers_menu(canvas)
        self.__draw_towers_upgrade_btns(canvas)

        if not self.__start:
            if self.__game_map.lives > 0:
                win = (pygame.font.SysFont(consts.TEXT_FONT_NAME, consts.TEXT_FONT_SIZE)
                             .render("You win", True, consts.TEXT_COLOR))


                canvas.blit(win, (self.__game_screen_size[0] + 50, (self.__game_screen_size[1]) / 2))
            else:
                win = (pygame.font.SysFont(consts.TEXT_FONT_NAME, consts.TEXT_FONT_SIZE)
                       .render("You lose", True, consts.TEXT_COLOR))

                canvas.blit(win, (self.__game_screen_size[0] + 50, (self.__game_screen_size[1]) / 2))

            self.__game_over[0].draw(canvas)
            self.__game_over[1].draw(canvas)

        if self.__start_btn is not None:
            self.__start_btn.draw(canvas)

    def update(self):
        if (self.__start and
                self.__wave_done and
                pygame.time.get_ticks() - self.__last_spawn >= consts.SPAWN_COOLDOWN):
            enemy = self.__game_map.wave(self.get_tile_size())
            if enemy is None:
                self.__wave_done = False
                self.__game_map.next_wave()
            else:
                self.__act_wave.add(EnemyView(enemy,
                                              ImageConvertor.get_img(enemy.name,
                                                                     self.get_tile_size())))

                # self.__act_wave = self.__enemies()
                # self.__wave_done = False
            self.__last_spawn =  pygame.time.get_ticks()

        if len(self.__act_wave) == 0 and self.__player_is_ready:
            self.__wave_done = True

        if self.__wave_done and self.__game_map.waves_done() or self.__game_map.lives <= 0:
            self.__start = False
            self.__is_towers_menu_visible = False
            self.__clicked_button = None
            self.__active_placed_tower = None

        if self.__start:
            self.__placed_towers.update(self.__game_map, self.__act_wave, self.__game_map.navigation_map, self.get_tile_size())
            self.__act_wave.update(self.__game_map, self.__game_screen_size)





    def get_tile_size(self):
        w = self.__game_map.width
        h = self.__game_map.height
        tile_w = round(self.__game_screen_size[0] / h)
        tile_h = round(self.__game_screen_size[1] / w)
        return (tile_w, tile_h)

    def event_handler(self, event):
        for tower_btn in self.__towers_group:
            if tower_btn.event_handler(event): # kliknutí na herní pole pro umístění věže
                # vykresit / skrýt nabídku věži
                if self.__clicked_button is tower_btn:
                    self.__is_towers_menu_visible = False
                    self.__clicked_button = None
                else:
                    self.__is_towers_menu_visible = True
                    self.__clicked_button = tower_btn
                self.__active_placed_tower = None

        # upgrady věží
        i = 0
        for upgrade_tower_menu_btn in self.__tower_upgrade_btns:
            if upgrade_tower_menu_btn.event_handler(event) and self.__active_placed_tower is not None:
                if self.__game_map.coins - consts.UPGRADE_COST >= 0:
                    if i == 0:
                        self.__active_placed_tower.tower.attack_damage += consts.UPGRADE_VAL
                        self.__game_map.coins -= consts.UPGRADE_COST
                    elif i == 1:
                        self.__active_placed_tower.tower.attack_range += consts.UPGRADE_VAL
                        self.__game_map.coins -= consts.UPGRADE_COST
                    elif i == 2 and self.__active_placed_tower.tower.attack_rate > 1:
                        self.__active_placed_tower.tower.attack_rate -= consts.UPGRADE_VAL
                        self.__game_map.coins -= consts.UPGRADE_COST
            i += 1

        if self.__start_btn is not None and self.__start_btn.event_handler(event):
            self.__player_is_ready = True
            self.__wave_done = True
            self.__start_btn.kill()
            self.__start_btn = None

        for tower_menu_btn in self.__tower_menu_btns:
            if tower_menu_btn[0].event_handler(event) and self.__clicked_button is not None:
                if self.__game_map.coins - tower_menu_btn[1].cost >= 0: # act tower
                    pos = self.__clicked_button.position
                    size = self.__clicked_button.size
                    self.__towers_group.remove(self.__clicked_button)
                    self.__clicked_button.kill()
                    self.__game_map.coins -= tower_menu_btn[1].cost
                    new_tower = Tower(
                        tower_menu_btn[1].name,
                        tower_menu_btn[1].attack_damage,
                        tower_menu_btn[1].attack_rate,
                        tower_menu_btn[1].attack_range,
                        tower_menu_btn[1].cost,
                    )

                    # správná počáteční orientace věže k herní cestě
                    new_tower.position = Position(pos[0] + size[0] / 2, pos[1] + size[1] / 2)
                    tile_size = self.get_tile_size()
                    tower_pos = Position(pos[1] // tile_size[1],
                                          pos[0] // tile_size[0])

                    path_pos = self.__game_map.navigation_map.get_game_path_pos(tower_pos)
                    if path_pos is None:
                        new_tower.angle = 0
                    else:
                        path_pos = Position(path_pos.y * self.get_tile_size()[0] + self.get_tile_size()[0] / 2,
                                            path_pos.x * self.get_tile_size()[1] + self.get_tile_size()[1] / 2)
                        vec = Position(path_pos.x - new_tower.position.x, path_pos.y - new_tower.position.y)
                        new_tower.angle = math.degrees(math.atan2(-vec.y, vec.x))

                    self.__placed_towers.add(TowerView(new_tower,
                                                       ImageConvertor.get_img(new_tower.name, (size[0] - consts.BASE_TOWER_DIFF, size[1] - consts.BASE_TOWER_DIFF)),
                                                       base_img=ImageConvertor.get_img("tower_base", size)))
                    self.__clicked_button = False
                    self.__is_towers_menu_visible = False


        for placed_tower in self.__placed_towers:
            if placed_tower.event_handler(event):
                if self.__active_placed_tower is placed_tower:
                    self.__active_placed_tower = None
                else:
                    self.__active_placed_tower = placed_tower
                    self.__is_towers_menu_visible = False
                    self.__clicked_button = None

        if not self.__start:
            if self.__game_over[0].event_handler(event): # play again
                return consts.PLAY_AGAIN
            if self.__game_over[1].event_handler(event): # game over
                return consts.BACK

        return consts.OK

    def draw_towers_menu(self, canvas):
        if not self.__is_towers_menu_visible:
            return
        height_pos = consts.TOWER_MENU_HEIGHT_POS
        for tower_elem in self.__tower_menu_btns:
            tower_elem[0].draw(canvas) # btn - ikona

            # název
            canvas.blit(tower_elem[2], (self.__game_screen_size[0] + consts.TOWER_VIEW_WIDTH + 40, height_pos))

            # damage, rate, range
            canvas.blit(tower_elem[3], (self.__game_screen_size[0] + consts.TOWER_VIEW_WIDTH + 40,
                                       height_pos + consts.TEXT_FONT_SIZE_DESCRIPTION))

            # cost
            canvas.blit(tower_elem[4], (self.__game_screen_size[0] + consts.TOWER_VIEW_WIDTH + 40,
                                       height_pos + 2 * consts.TEXT_FONT_SIZE_DESCRIPTION))

            height_pos += 2 * consts.TEXT_FONT_SIZE_DESCRIPTION + 25

    def __draw_towers_upgrade_btns(self, canvas):
        if self.__active_placed_tower is None:
            return
        height_pos = consts.TOWER_MENU_HEIGHT_POS + 3 * consts.BTN_UPG_HEIGHT + 5
        [atc_btn, range_btn, rate_btn] = self.__tower_upgrade_btns

        atc_btn.draw(canvas)

        range_btn.draw(canvas)

        rate_btn.draw(canvas)

        tower_info1 = (pygame.font.SysFont(consts.TEXT_FONT_NAME, consts.TEXT_FONT_SIZE_DESCRIPTION)
                        .render("Tower name: " + str(self.__active_placed_tower.tower.name), True, consts.TEXT_COLOR))

        tower_info2 = (pygame.font.SysFont(consts.TEXT_FONT_NAME, consts.TEXT_FONT_SIZE_DESCRIPTION)
                        .render("Damage: " + str(self.__active_placed_tower.tower.attack_damage), True, consts.TEXT_COLOR))

        tower_info3 = (pygame.font.SysFont(consts.TEXT_FONT_NAME, consts.TEXT_FONT_SIZE_DESCRIPTION)
                        .render("Rate: " + str(self.__active_placed_tower.tower.attack_rate), True, consts.TEXT_COLOR))

        tower_info4 = (pygame.font.SysFont(consts.TEXT_FONT_NAME, consts.TEXT_FONT_SIZE_DESCRIPTION)
                        .render("Range: " + str(self.__active_placed_tower.tower.attack_range), True, consts.TEXT_COLOR))

        canvas.blit(tower_info1, (self.__game_screen_size[0] + 40, height_pos + 3 * consts.TEXT_FONT_SIZE_DESCRIPTION))
        canvas.blit(tower_info2, (self.__game_screen_size[0] + 40, height_pos + 4 * consts.TEXT_FONT_SIZE_DESCRIPTION))
        canvas.blit(tower_info3, (self.__game_screen_size[0] + 40, height_pos + 5 * consts.TEXT_FONT_SIZE_DESCRIPTION))
        canvas.blit(tower_info4, (self.__game_screen_size[0] + 40, height_pos + 6 * consts.TEXT_FONT_SIZE_DESCRIPTION))

    def __create_towers_menu(self):
        lst = []
        height_pos = consts.TOWER_MENU_HEIGHT_POS
        for act_tower in self.__game_map.available_towers:
            tower_img = ImageConvertor.get_img(act_tower.name,
                                   (consts.TOWER_VIEW_WIDTH,
                                         consts.TOWER_VIEW_HEIGHT))

            tower_btn = Button((self.__game_screen_size[0] + 20, height_pos),
                        (consts.TOWER_VIEW_WIDTH, consts.TOWER_VIEW_HEIGHT),
                           image = tower_img,
                           pos_mid=False)


            tower_name = (pygame.font.SysFont(consts.TEXT_FONT_NAME, consts.TEXT_FONT_SIZE_DESCRIPTION)
                           .render("Tower name: " + str(act_tower.name), True, consts.TEXT_COLOR))

            tower_damage = (pygame.font.SysFont(consts.TEXT_FONT_NAME, consts.TEXT_FONT_SIZE_DESCRIPTION)
                            .render("Damage: " + str(act_tower.attack_damage) +
                                    " Rate: " + str(act_tower.attack_rate) +
                                    " Range: " + str(act_tower.attack_range) , True, consts.TEXT_COLOR))

            tower_cost = (pygame.font.SysFont(consts.TEXT_FONT_NAME, consts.TEXT_FONT_SIZE_DESCRIPTION)
                            .render("Cost: " + str(act_tower.cost) , True, consts.TEXT_COLOR))

            lst.append((tower_btn, act_tower, tower_name, tower_damage, tower_cost))
            height_pos += 2 * consts.TEXT_FONT_SIZE_DESCRIPTION + 25
        return lst

    def __create_upgrade_view(self):
        height_pos = consts.TOWER_MENU_HEIGHT_POS

        upg_atc_btn = Button((self.__game_screen_size[0] + 30, height_pos),
                        (consts.BTN_UPG_WIDTH, consts.BTN_UPG_HEIGHT),
                           bg_color=consts.BTN_BG_COLOR2,
                           font_size = consts.BTN_UPG_FONT_SIZE,
                           text = "Upgrade attack damage",
                           pos_mid = False)

        upg_rng_btn = Button((self.__game_screen_size[0] + 30, height_pos + consts.BTN_UPG_HEIGHT + 10),
                        (consts.BTN_UPG_WIDTH, consts.BTN_UPG_HEIGHT),
                           bg_color=consts.BTN_BG_COLOR2,
                           font_size = consts.BTN_UPG_FONT_SIZE,
                           text = "Upgrade attack range",
                           pos_mid = False)

        upg_rt_btn = Button((self.__game_screen_size[0] + 30, height_pos + 2 * consts.BTN_UPG_HEIGHT + 20),
                        (consts.BTN_UPG_WIDTH, consts.BTN_UPG_HEIGHT),
                           bg_color=consts.BTN_BG_COLOR2,
                           text = "Upgrade attack rate",
                           font_size = consts.BTN_UPG_FONT_SIZE,
                           pos_mid = False)

        return (upg_atc_btn, upg_rng_btn, upg_rt_btn)


    def __create_game_over_view(self):
        play_again_btn = Button((self.__game_screen_size[0] + 30, self.__game_screen_size[1] - 20 - 2 * consts.BTN_CTRL_HEIGHT),
                        (consts.BTN_UPG_WIDTH, consts.BTN_UPG_HEIGHT),
                           bg_color=consts.BTN_BG_COLOR2,
                           text = "Play again",
                           font_size = consts.BTN_UPG_FONT_SIZE,
                           pos_mid = False)


        back_to_menu_btn = Button((self.__game_screen_size[0] + 30, self.__game_screen_size[1] - 10 - consts.BTN_CTRL_HEIGHT),
                        (consts.BTN_UPG_WIDTH, consts.BTN_UPG_HEIGHT),
                           bg_color=consts.BTN_BG_COLOR2,
                           font_size = consts.BTN_UPG_FONT_SIZE,
                           text = "Back to menu",
                           pos_mid = False)
        return (play_again_btn, back_to_menu_btn)