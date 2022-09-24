import random
from files.blocks.blocks_man import Blocks_manager
from files.terrain.structure import Structure
from files.vars import structure_manager_list

class Leaves(Blocks_manager):
    
    def __init__(self):
        Blocks_manager.__init__(self)

        self.block_id = 6
        self.blocks_parents = [
            (0,0),
            (0,1)
        ]
        self.durability = 15
        self.colored = (40, random.randint(51, 200),0)