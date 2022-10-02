import random


class MonsterManager(list):
    def __init__(self, dungeon):
        super().__init__()
        self.dungeon = dungeon

    def add_multiple(self, type, amount):
        for _ in range(amount):
            randx = random.randrange(self.dungeon.tile_size, self.dungeon.width*self.dungeon.tile_size)
            randy = random.randrange(self.dungeon.tile_size, self.dungeon.height*self.dungeon.tile_size)
            
            self.append((type, randx, randy))