from files.blocks.blocks_man import Blocks_manager

class Bedrock(Blocks_manager):
    
    def __init__(self, App):
        Blocks_manager.__init__(self, App)

        self.block_id = 4
        self.durability = False