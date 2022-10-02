import pygame

from equipment.equipment import Equipment

from inventory.EntityInventory import EntityInventory

class PlayerInventory(EntityInventory):
    def __init__(self):
        super().__init__(45)

    def draw(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        padding_left = 500
        padding_top = 25
        size = 50
        spacing = 5
        

        for item_number, item in enumerate(self.hotbar):
            left = padding_left + size*item_number + spacing*item_number
            
            if item_number == self.equipped_index:
                frame_colour = (255, 255, 255)
            else:
                frame_colour = (255, 0, 0)
            
            pygame.draw.rect(screen, frame_colour, (left, padding_top, size, size), 2)

            if item is not None:
                if "image" in item.__dict__.keys():
                    screen.blit(item.image, (left, padding_top))

    def update_inventory(self, screen, events, keys, dt, dungeon, cameraX, cameraY):
        super().update_inventory(screen, events, keys, dt, dungeon, cameraX, cameraY)

        if isinstance(self.equipped_item, Equipment):
            self.equipped_item.update(screen, events, keys, dt, dungeon, cameraX, cameraY)

        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                if event.y == -1:
                    self.equipped_index += 1

                    if self.equipped_index == len(self.hotbar):
                        self.equipped_index = 0

                    self.equipped_item = self.items[self.equipped_index]

                if event.y == 1:
                    self.equipped_index -= 1

                    if self.equipped_index == -1:
                        self.equipped_index = len(self.hotbar) - 1

                    self.equipped_item = self.items[self.equipped_index]

        self.draw(screen, events, keys, dt, dungeon, cameraX, cameraY)