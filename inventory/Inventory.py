from equipment.equipment import Equipment


class Inventory():
    def __init__(self, size=16):
        super().__init__()

        self.items = []

        for _ in range(size):
            self.items.append(None)

    def remove_item_by_index(self, index):
        self.items[index] = None

    def remove_item_by_name(self, name):
        for item_number, item in enumerate(self.items):
            if item.name == name:
                self.remove_item_by_index(item_number)
                break

    def remove_items_by_name(self, name):
        for item_number, item in enumerate(self.items):
            if item.name == name:
                self.remove_item_by_index(item_number)