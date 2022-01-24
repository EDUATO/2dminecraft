import pygame
from files.functions import convert_blocks_pos_to_camera_xy, convert_camera_xy_to_block_pos, toNegative
from files.vars import block_scale_buff, block_size

class Chunk:
    def __init__(self, id, size):
        self.Chunk_ID = id
        self.size = size
        self.x_block_start_pos = id * size[0]

        # Keep in mind that they are screen_pos
        self.initial_pos = convert_blocks_pos_to_camera_xy(grid_pos=(self.x_block_start_pos, 0))
        self.block_size = convert_blocks_pos_to_camera_xy(grid_pos=self.size)

        self.chunkBlockRect = (
            self.initial_pos[0],
            self.initial_pos[1],
            -self.block_size[0],
            self.block_size[1]
        )

    def isRectInChunk(self,surface, camera, Rect):
        chunk_limit = self.ChunkLimits(camera)

        if Rect.colliderect(pygame.Rect(chunk_limit)):
            return True

        return False

    def ChunkLimits(self, camera):
        # Convert blocks coords to camera_xy
        block_position = convert_blocks_pos_to_camera_xy(grid_pos=(self.x_block_start_pos, 0))[0]
        size = convert_blocks_pos_to_camera_xy(grid_pos=(self.size[0], self.size[1]-1))
        
        chunk_camera_pos = toNegative(camera.convert_screen_pos_to_camera_xy(screen_pos=(block_position, size[1])))

        return (chunk_camera_pos[0], chunk_camera_pos[1], self.chunkBlockRect[2], self.chunkBlockRect[3])

    def DrawChunkLimits(self,surface, camera):
        #print(self.Chunk_ID)
        """ Draw the chunk borders in the game """
        chunks_limits = self.ChunkLimits(camera)

        # Draw the lines
        pygame.draw.line(surface, (255,255,0), (chunks_limits[0], chunks_limits[1]), (chunks_limits[0], chunks_limits[1] + chunks_limits[3]), width=2) # First
        pygame.draw.line(surface, (255,255,0), (chunks_limits[0], chunks_limits[2]), (chunks_limits[1], chunks_limits[3]), width=2) # Second

    def get_chunk_id(self):
        return self.Chunk_ID

    def get_size(self):
        return self.size

    def get_chunkBlockRect(self):
        return self.chunkBlockRect

    def get_x_block_start_pos(self):
        return self.x_block_start_pos
