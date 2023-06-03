from files.blocks.blocks_man import Blocks_manager
from files.terrain.structure import Structure

class WoodenPlanks(Blocks_manager):
    
    def __init__(self, App):
        Blocks_manager.__init__(self, App)

        self.block_id = 9
        self.durability = 100