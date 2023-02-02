from files.blocks.blocks_man import Blocks_manager
from files.gui.Inventory import Inventory

class Chest(Blocks_manager):
    
    def __init__(self):
        Blocks_manager.__init__(self)

        self.block_id = 11
        self.durability = 120

        self.Inventory = Inventory()

    def rightClickAction(self, block, game):
        self.Inventory.open()