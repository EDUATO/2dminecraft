from files.functions import convert_blocks_pos_to_camera_xy

class Chunk:
    def __init__(self, id, size, x_start_pos):
        self.Chunk_ID = id
        self.size = size
        self.x = x_start_pos

        self.initial_pos = convert_blocks_pos_to_camera_xy(grid_pos=(self.x, 0)) 
        self.block_size = convert_blocks_pos_to_camera_xy(grid_pos=self.size)
        self.chunkBlockRect = (
            self.initial_pos[0],
            self.initial_pos[1],
            self.block_size[0],
            self.block_size[1]
        )

    def get_chunk_id(self):
        return self.Chunk_ID

    def get_size(self):
        return self.size

    def get_chunkBlockRect(self):
        return self.chunkBlockRect