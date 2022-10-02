from copy import deepcopy
import pygame
from Manager import Manager
from entities.monster.MonsterManager import MonsterManager
from gui.impl.GuiMainMenu import GuiMainMenu
from player import player

class Dungeon:
    def __init__(self, name, required_level:int=0):
        self.name = name
        
        self.monster_supply = MonsterManager(self)

        self.monsters = []

        self.width = 10
        self.height = 10

        self.required_level = required_level

        self.tile_size = 100

        self.floor = None

        player.cameraX = self.width*self.tile_size / 2 - 300
        player.cameraY = self.height*self.tile_size / 2 - 300

        self.time_until_end = 5

    def load_monsters(self):
        stat_multiplier = (player.level + 9) / 10
        for monster in self.monster_supply:
            _monster = monster[0](monster[1], monster[2])

            _monster.health *= stat_multiplier
            _monster.max_health *= stat_multiplier

            _monster.physical_damage *= stat_multiplier
            _monster.magical_damage *= stat_multiplier
            
            self.monsters.append(_monster)
        
    def update(self, screen, events, keys, dt, no_draw):
        for event in events:
            if event.type == pygame.USEREVENT+2:
                self.time_until_end -= 1
                player.time_until_end = self.time_until_end
                player.update_time_ending_text()

                if self.time_until_end == -1:
                    player.time_until_end = 5
                    self.time_until_end = 5
                    player.time_ending = False
                    player.update_time_ending_text()
                    Manager.get_manager("OverlayManager").clear_stack()
                    Manager.get_manager("GuiManager").current_gui = GuiMainMenu()

        if self.floor is not None and not no_draw:
            left = int(player.cameraX // self.tile_size)
            top = int(player.cameraY // self.tile_size)

            sr = screen.get_rect()

            for x in range(left, sr.width//self.tile_size+left+1):
                for y in range(top, sr.height//self.tile_size+top+1):
                    fx = x*self.tile_size
                    fy = y*self.tile_size

                    if fx > 0 and fy > 0 and fx < (self.width+1)*self.tile_size and fy < (self.height+1)*self.tile_size:
                        screen.blit(self.floor, (fx-player.cameraX, fy-player.cameraY))

        for monster_number, monster in enumerate(self.monsters):
            if monster.health > 0:
                if player.can_see(monster):
                    if not no_draw:
                        monster.update(screen, events, keys, dt, self, player.cameraX, player.cameraY)
            else:
                del self.monsters[monster_number]
                player.award_exp(monster.max_health / 10 + max(monster.physical_damage, monster.magical_damage))

                if len(self.monsters) == 0:
                    player.time_ending = True
                    pygame.time.set_timer(pygame.USEREVENT+2, 1000, 6)

        if not no_draw:
            player.update(screen, events, keys, dt, self)