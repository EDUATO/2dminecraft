class Blocks_manager:
    def __init__(self):
        self.block_id = None

        self.blocks_parents = [ 
            (0, 0)
        ]

    def place_block(self, grid_pos, chunks_list):
        grid_positions = self.get_blocks_parents_grid_pos(center_grid_pos=grid_pos)

        blocks_to_place = self.seek_block_position(chunks_list, grid_positions)
        if blocks_to_place != False:
            for b in range(len(blocks_to_place)):
                blocks_to_place[b].setBlock(id=self.block_id)

    def break_block(self,surface, grid_pos, chunks_list, deltaTime):
        grid_positions = self.get_blocks_parents_grid_pos(center_grid_pos=grid_pos)

        blocks_to_break = self.seek_block_position(chunks_list, grid_positions)
        if blocks_to_break != False:
            for b in range(len(blocks_to_break)):
                blocks_to_break[b].breakBlock(surface, deltaTime)


    def seek_block_position(self, chunks_list, grid_pos:tuple):
        blocks_positions = []

        for c in range(len(chunks_list)):
            for i in range(len(chunks_list[c].blocks)):

                for g in range(len(grid_pos)):
                    if chunks_list[c].blocks[i].getGridCoords() == grid_pos[g]:
                        blocks_positions.append(chunks_list[c].blocks[i])

        if blocks_positions != []:
            return blocks_positions
        
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