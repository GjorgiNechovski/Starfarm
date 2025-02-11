class InventoryItem:
    def __init__(self, item_type, image, name, quantity, price, energy_restore=0):
        self.item_type = item_type
        self.image = image
        self.name = name
        self.quantity = quantity
        self.price = price
        self.energy_restore = energy_restore  # How much energy this item restores

    def is_tool(self):
        return self.item_type == "tool"