from json import load
import math
import random
from items.equipment.Rarities import Rarities

from items.equipment.equipment import Equipment
from util.ResourceLocation import ResourceLocation

from player import player

from config import *

class Weapon(Equipment):
    ATTACK_COOLDOWN = pygame.USEREVENT + 1

    def __init__(self, json) -> None:
        super().__init__(json, load(open(ResourceLocation("assets/playerdata/default-weapon-stats.json"))))
        self.json = json

        self.rarity = Rarities.get_random_rarity()

        self.attack_speed = 0.5
        self.heavy_attack_speed = 1

        self.attack_range = 250

        self.ice = 0
        self.fire = 0
        self.toxin = 0
        self.bleeding = 0

        self.can_attack = True

        self.heavy_attack_damage_multiplier = 1.5

    def instance(self):
        return Weapon(self.json)

    def get_monsters_in_range(self, dungeon):
        in_range = []

        for monster in dungeon.monsters:
            mx = monster.x - player.cameraX + monster.width / 2
            my = monster.y - player.cameraY + monster.height / 2

            px = player.x + player.width / 2
            py = player.y + player.height / 2

            dx, dy = abs(px-mx), abs(py-my)

            if math.sqrt(dx**2+dy**2) <= self.attack_range:
                in_range.append(monster)
        
        return in_range

    def on_normal_attack(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        damage = player.physical_damage

        crit = random.randrange(0, 101)
        if crit <= player.critical_chance:
            damage *= player.critical_multiplier

        monsters = self.get_monsters_in_range(dungeon)
        
        for monster in monsters:
            monster.health -= damage

        return monsters

    def on_heavy_attack(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        damage = player.physical_damage*self.heavy_attack_damage_multiplier

        crit = random.randrange(0, 101)
        if crit <= player.critical_chance:
            damage *= player.critical_multiplier

        monsters = self.get_monsters_in_range(dungeon)
        
        for monster in monsters:
            monster.health -= damage

        return monsters


    def update(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        super().update(screen, events, keys, dt, dungeon, cameraX, cameraY)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == NORMAL_ATTACK:
                    if self.can_attack:
                        cooldown = int(self.attack_speed*1000)
                        print(player.attackspeedmultiplier)
                        pygame.time.set_timer(Weapon.ATTACK_COOLDOWN, cooldown)
                        self.on_normal_attack(screen, events, keys, dt, dungeon, cameraX, cameraY)
                        self.can_attack = False
                
                if event.key == HEAVY_ATTACK:
                    if self.can_attack:
                        pygame.time.set_timer(Weapon.ATTACK_COOLDOWN, int(self.heavy_attack_speed*1000/player.attackspeedmultiplier))
                        self.on_heavy_attack(screen, events, keys, dt, dungeon, cameraX, cameraY)
                        self.can_attack = False
        
            if event.type == Weapon.ATTACK_COOLDOWN:
                self.can_attack = True

    @staticmethod
    def load_data_from_file(weapon_name):
        return load(open(ResourceLocation(f"assets/itemdata/{weapon_name}.json")))

    @staticmethod
    def fromRegistryName(name:str):
        return Weapon(Weapon.load_data_from_file(name))