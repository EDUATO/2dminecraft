from files.blocks.blocks_man import Blocks_manager

class Stone(Blocks_manager):
    
    def __init__(self):
        Blocks_manager.__init__(self)

        self.block_id = 2
        self.durability = 200

    def rightClickAction(self, block, game):
        entity_classes = game.Entities_man.getEntitiesClasses()
        for i in range(len(entity_classes)):
            if entity_classes[i].get_uuid() == game.p1_uuid:
                entity_classes[i].EntityInventory.open()