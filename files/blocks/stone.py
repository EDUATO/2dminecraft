from files.blocks.blocks_man import Blocks_manager

class Stone(Blocks_manager):
    
    def __init__(self, App):
        Blocks_manager.__init__(self, App)

        self.block_id = 2
        self.durability = 200

    def rightClickAction(self, block, game):
        pass