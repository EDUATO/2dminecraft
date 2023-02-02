from files.blocks.blocks_man import Blocks_manager


class StoneBricks(Blocks_manager):
    
    def __init__(self):
        Blocks_manager.__init__(self)

        self.block_id = 10
        self.durability = 200
    
