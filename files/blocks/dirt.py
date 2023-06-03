from files.blocks.blocks_man import Blocks_manager

class Dirt(Blocks_manager):
    
    def __init__(self, App):
        Blocks_manager.__init__(self, App)

        self.block_id = 3
        self.durability = 35