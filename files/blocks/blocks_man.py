class Blocks_manager:
    def __init__(self):
        self.block_id = None

        self.blocks_parents = [ 
            (0, 0)
        ]
        self.colored = False
        self.durability = 1

    def generate_structure(self, position):
        pass

    def __place_data__(self, block):
        self.__init__()
        block.setBlock(id=self.block_id)
        block.set_colored_sprite(self.colored)
        block.break_durability = self.durability
        position = block.getGridCoords()
        self.generate_structure(position)
    
    def place_block(self, grid_pos, chunks_list):
        grid_positions = self.get_blocks_parents_grid_pos(center_grid_pos=grid_pos)

        blocks_to_place = self.seek_several_blocks_positions(chunks_list, grid_positions)
        if blocks_to_place != False:
            for b in range(len(blocks_to_place)):
                self.__place_data__(blocks_to_place[b])

    def place_generated_block(self, block):
        self.__place_data__(block)

    def break_block(self,surface, grid_pos, chunks_list, deltaTime):
        blocks_to_break = self.seek_one_block_position(chunks_list, grid_pos)
        if blocks_to_break != False:
            blocks_to_break.breakBlock(surface, deltaTime)


    def seek_several_blocks_positions(self, chunks_list, grid_pos:tuple):
        blocks_positions = []
        
        for c in range(len(chunks_list)):
            for i in range(len(chunks_list[c].blocks)):

                for g in range(len(grid_pos)):
                    if chunks_list[c].blocks[i].getGridCoords() == grid_pos[g]:
                        blocks_positions.append(chunks_list[c].blocks[i])

        if blocks_positions != []:
            return blocks_positions
        
        return False

    def seek_one_block_position(self, chunks_list, grid_pos):
        block_position = None
        
        for c in range(len(chunks_list)):
            for i in range(len(chunks_list[c].blocks)):

                if chunks_list[c].blocks[i].getGridCoords() == grid_pos:
                    block_position = chunks_list[c].blocks[i]
                    break

            if block_position != None:
                return block_position

        return False

    def get_blocks_parents_grid_pos(self, center_grid_pos):
        output = []
        
        for i in range(len(self.blocks_parents)):
            _tuple = []

            # -X- and -Y-
            for co in range(2):
                _tuple.append(center_grid_pos[co] + self.blocks_parents[i][co])

            output.append(tuple(_tuple))

        return tuple(output)