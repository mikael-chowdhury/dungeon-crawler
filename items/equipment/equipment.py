from items.Item import Item


class Equipment(Item):
    def __init__(self, json, basejson) -> None:
        super().__init__(json, basejson)

    def update(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        pass

    def get_player_buffs(self):
        return self.json["player-buffs"] if "player-buffs" in self.json.keys() else {}

    def get_modifiers(self) -> dict:
        return self.json["modifiers"] if "modifiers" in self.json.keys() else {}