from files.blocks.blocks_man import Blocks_manager

class Stone(Blocks_manager):
    
    def __init__(self):
        Blocks_manager.__init__(self)

        self.block_id = 2