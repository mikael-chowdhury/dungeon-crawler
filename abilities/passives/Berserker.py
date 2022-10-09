from abilities.passives.Passive import Passive

from player import player

class Berserker(Passive):
    def __init__(self):
        super().__init__("Berserker", "berserker")

        player.physical_damage = int(player.physical_damage * 1.2)
        player.attackspeedmultiplier = int(player.attackspeedmultiplier * 1.2)