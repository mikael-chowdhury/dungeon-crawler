
from copy import deepcopy
import json
import pygame
from config import ANTIALIASING
from entities.Entity import Entity
from font.FontManager import FontManager
from gui.GuiManager import GuiManager
from inventory.PlayerInventory import PlayerInventory
from ui.items.StatusBar import StatusBar
from util.ResourceLocation import ResourceLocation
from math import atan2, pi, degrees

from gui.impl.GuiGameOver import GuiGameOver

import config

class Player(Entity):
    def __init__(self):
        super().__init__(0, 0)

        self.DEFAULT_STATS = json.load(open(ResourceLocation("assets/playerdata/default-stats.json")))

        self.health = self.DEFAULT_STATS["max_health"]

        self.cameraX = 0
        self.cameraY = 0

        self.exp = 0
        self.level = 1
        self.required_exp = self.get_required_exp()
        
        self.passives:list = [None, None, None, None, None]
        self.passiveInventory:list = [None for _ in range(45)]

        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        rect.center = (400, 400)
        self.set_rect(rect)

        self.original_image = pygame.transform.smoothscale(pygame.image.load(ResourceLocation("assets/textures/entities/male-character.png")), (self.width, self.height))
        self.image = self.original_image
        
        self.inventory = PlayerInventory()

        self.first_load = True

        self.rotation_padding = 270

        self.level_font = None
        self.level_text = None

        self.time_until_end = 5
        self.time_ending_text = None
        self.time_ending_font = None
        self.time_ending = False

        self.exp_star = None

        self.lifesteal = 0

        self.is_dead = False

    def recieve_damage(self, amount):
        self.health -= amount
        
        if self.health <= 0:
            self.is_dead = True

    def movement(self, keys, dt, dungeon):
        up = keys[pygame.K_w] or keys[pygame.K_UP]
        down = keys[pygame.K_s] or keys[pygame.K_DOWN]
        left = keys[pygame.K_a] or keys[pygame.K_LEFT]
        right = keys[pygame.K_d] or keys[pygame.K_RIGHT]

        move = pygame.math.Vector2(right-left, down-up)
        if move.length_squared() > 0:
            move.scale_to_length(self.speed*dt)
        
        if move[0] < 0:
            if self.rect.x + self.cameraX - self.width > 0:
                self.cameraX += move[0]
        if move[0] > 0:
            if self.rect.x + self.cameraX < dungeon.width * dungeon.tile_size:
                self.cameraX += move[0]

        if move[1] < 0:
            if self.rect.y + self.cameraY - self.width > 0:
                self.cameraY += move[1]

        if move[1] > 0:
            if self.rect.y + self.cameraY < dungeon.height * dungeon.tile_size:
                self.cameraY += move[1]

    def draw_attack_range_circle(self, screen):
        if self.inventory.equipment.weapon is not None and "attack_range" in self.inventory.equipment.weapon.__dict__.keys():
            range = self.inventory.equipment.weapon.attack_range
        else:
            range = 0

        if range > 0:
            surface = pygame.Surface((800, 800), pygame.SRCALPHA)
            pygame.draw.circle(surface, (255, 0, 0, 25), self.rect.center, range)
            screen.blit(surface, (0,0))
        pass

    def draw_player_level(self, screen):
        if self.first_load:
            self.level_font = FontManager.VT323_36
            self.level_text = self.level_font.render(str(self.level), ANTIALIASING, (214, 209, 45))
        else:
            screen.blit(self.exp_star, (5, 10))
            screen.blit(self.level_text, (40, 10))

    def update_level_text(self):
        if self.level_font is not None:
            self.level_text = self.level_font.render(str(self.level), ANTIALIASING, (214, 209, 45))

    def draw_status_bars(self, screen, events, keys, dt, dungeon):
        self.health_bar.update(screen, events, keys, dt, dungeon)
        self.mana_bar.update(screen, events, keys, dt, dungeon)
        self.xp_bar.update(screen, events, keys, dt, dungeon)

    def update_time_ending_text(self):
        if self.time_ending_font is not None:
            self.time_ending_text = self.time_ending_font.render(str(self.time_until_end), ANTIALIASING, (255, 0, 0))

    def draw_time_ending_text(self, screen):
        if self.first_load:
            self.time_ending_font = FontManager.VT323_64
            self.time_ending_text = self.time_ending_font.render(str(self.time_until_end), ANTIALIASING, (255, 0, 0))
        else:
            if self.time_ending:
                rect = self.time_ending_text.get_rect(center=(40, 100))
                screen.blit(self.time_ending_text, rect)

    def get_angle(self, origin, destination):
        x_dist = destination[0] - origin[0]
        y_dist = destination[1] - origin[1]
        return atan2(-y_dist, x_dist) % (2 * pi)

    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def update(self, screen, events, keys, dt, dungeon):
        for event in events:
            if event.type == pygame.USEREVENT + 5:
                if player.mana < player.max_mana:
                    player.mana += player.mana_gain_speed

        if self.is_dead:
           from Manager import Manager
           guimanager:GuiManager = Manager.get_manager("GuiManager")
           guimanager.current_gui = GuiGameOver()
            
        angle = self.get_angle((self.rect.center), pygame.mouse.get_pos())
        self.image = self.rot_center(self.original_image, degrees(angle)+self.rotation_padding).convert_alpha()
        
        if self.first_load:
            pygame.time.set_timer(pygame.USEREVENT + 5, 1000)

            self.exp_star = pygame.image.load(ResourceLocation("assets/ui/star.png")).convert_alpha()

            self.health_bar = StatusBar(None, 22, 706, 130, 20, background_image=pygame.image.load(ResourceLocation("assets/ui/health_bar.png")).convert_alpha(), status=self.health, total=self.max_health, line_start=25, line_end=95, bar_colour=(255, 0, 0))
            self.mana_bar = StatusBar(None, 25, 728, 126, 26, background_image=pygame.image.load(ResourceLocation("assets/ui/mana_bar.png")).convert_alpha(), status=self.mana, total=self.max_mana, line_start=22, line_end=90, bar_colour=(0, 97, 255))
            self.xp_bar = StatusBar(None, 25, 750, 126, 26, background_image=pygame.image.load(ResourceLocation("assets/ui/xp_bar.png")).convert_alpha(), status=self.exp, total=self.required_exp, line_start=25, line_end=95, bar_colour=(0, 255, 255))

        self.health_bar.status = self.health
        self.health_bar.total = self.max_health

        self.mana_bar.status = self.mana
        self.mana_bar.total = self.max_mana

        self.xp_bar.status = self.exp
        self.xp_bar.total = self.required_exp

        self.draw_attack_range_circle(screen)
        self.inventory.load_stat_boosters(self)

        for passive in [x for x in self.passives if x is not None]:
            passive.apply(passive.level, self)

        self.position_facing = pygame.mouse.get_pos()
        self.movement(keys, dt, dungeon)
        super().update(screen, events, keys, dt, dungeon, 0, 0)
        self.draw_status_bars(screen, events, keys, dt, dungeon)
        self.draw_player_level(screen)
        self.draw_time_ending_text(screen)

        srect = screen.get_rect()
        y = 5
        for passive in self.passives:
            if passive is not None:
                rect = passive.image.get_rect(right=srect.right - 5)
                screen.blit(passive.image, (rect.x, y))
                y += rect.height + 5

        self.first_load = False

    def can_see(self, entity):
        ws = pygame.display.get_window_size()
        return entity.x-self.cameraX+entity.width >= 0 and entity.x-self.cameraX <= ws[0] and entity.y+entity.height-self.cameraY >= 0 and entity.y-self.cameraY <= ws[1]

    def reset_stats(self):
        for stat in dict(self.DEFAULT_STATS).keys():
            setattr(self, stat, self.DEFAULT_STATS[stat])

    def get_required_exp(self):
        return config.XP(self.level)

    def award_exp(self, exp):
        self.exp += exp
        prevexp = deepcopy(self.exp)
        prev = deepcopy(self.required_exp)

        if self.exp >= self.required_exp:
            self.level += 1
            self.update_level_text()
            self.required_exp = self.get_required_exp()
            self.exp = 0
            self.award_exp(prevexp-prev)

    def givehealth(self, amount):
        self.health += amount

        if self.health > self.max_health:
            self.health = self.max_health

    def give_passive(self, passive):
        for index, p in enumerate(self.passiveInventory):
            if p is None:
                self.passiveInventory[index] = passive
                break
            
player = Player()