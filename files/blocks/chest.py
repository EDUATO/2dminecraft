from files.blocks.blocks_man import Blocks_manager
from files.gui.chest_gui import ChestContainer

# TODO : Make each block independant

class Chest(Blocks_manager):
    
    def __init__(self, App):
        Blocks_manager.__init__(self, App)

        self.block_id = 11
        self.durability = 120

        self.chestInventory = ChestContainer(App)

    def rightClickAction(self, block, game):
        self.chestInventory.open()