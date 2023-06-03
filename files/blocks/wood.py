from files.blocks.blocks_man import Blocks_manager
from files.terrain.structure import Structure
from files.vars import structure_manager_list

class Wood(Blocks_manager):
    
    def __init__(self, App):
        Blocks_manager.__init__(self, App)

        self.block_id = 5
        self.durability = 120