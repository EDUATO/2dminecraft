import pygame
import math

from files.functions import convert_blocks_pos_to_camera_xy, convert_camera_xy_to_block_pos, toNegative
from files.vars import block_scale_buff, block_size, chunk_size
from files.blocks.Block import Block
from files.camera import Camera

class Chunk:
    def __init__(self, id):
        self.Chunk_ID = id
        self.x_block_start_pos = self.Chunk_ID * chunk_size[0]

        # Keep in mind that they are screen_pos
        self.initial_pos = convert_blocks_pos_to_camera_xy(grid_pos=(self.x_block_start_pos, 0))
        self.block_size = convert_blocks_pos_to_camera_xy(grid_pos=chunk_size)

        self.chunkBlockRect = (
            self.initial_pos[0],
            self.initial_pos[1],
            -self.block_size[0],
            self.block_size[1]
        )

        # Will handle all the blocks that are part of the chunk
        self.blocks = []

    def generate(self, blocks_list_to_generate:list):
        """ 
        Will generate air blocks for the chunk 
        - blocks_list_to_generate must be as long as chunk_size[0]* chunk_size[1]
        """
        block_gen_index = 0
        for y in range( chunk_size[1] ):
            for x in range( chunk_size[0] ):
                POSITION = (x + chunk_size[0]*self.Chunk_ID, y)
                self.blocks.append(
                    Block(block_pos_grid=POSITION) 
                )
                bks = blocks_list_to_generate[block_gen_index]
                self.blocks[len(self.blocks)-1].setBlock(id=0,color=(0,0, 1 * bks["color"]),noiseValue=bks["noise"] )
                block_gen_index += 1

    def isRectInChunk(self,surface, camera, Rect):
        """ Is rect INSIDE the chunk? """
        chunk_limit = self.ChunkLimits(camera)

        return Rect.colliderect(pygame.Rect(chunk_limit))

    def is_rect_in_chunk_x_coords(self, surface, camera, Rect):
        """ Is rect in the x_coords of the chunk? (not necessarily in the interior) """
        chunk_limit = self.ChunkLimits(camera)
    
        if (Rect.x + Rect.width) >= chunk_limit[0] and (Rect.x + Rect.width) < (chunk_limit[0] + chunk_limit[2]):
            return True

        return False

    def ChunkLimits(self, camera):
        # Convert blocks coords to camera_xy
        block_position = convert_blocks_pos_to_camera_xy(grid_pos=(self.x_block_start_pos, 0))[0]
        size = convert_blocks_pos_to_camera_xy(grid_pos=(chunk_size[0], chunk_size[1]-1))
        
        chunk_camera_pos = toNegative(camera.convert_screen_pos_to_camera_xy(screen_pos=(block_position, size[1])))

        return (chunk_camera_pos[0], chunk_camera_pos[1], self.chunkBlockRect[2], self.chunkBlockRect[3])

    def DrawChunkLimits(self,surface, camera):
        """ Draw the chunk borders in the game """
        chunks_limits = self.ChunkLimits(camera)

        # Draw the lines
        pygame.draw.line(surface, (255,255,0), (chunks_limits[0], chunks_limits[1]), (chunks_limits[0], chunks_limits[1] + chunks_limits[3]), width=2) # First
        pygame.draw.line(surface, (255,255,0), (chunks_limits[0], chunks_limits[2]), (chunks_limits[1], chunks_limits[3]), width=2) # Second

    def get_block(self, position:tuple):
        for block in self.blocks:
            if block.getGridCoords() == tuple(position):
                return block

    def get_chunk_id(self):
        return self.Chunk_ID

    def get_size(self):
        return self.size

    def get_chunkBlockRect(self):
        return self.chunkBlockRect

    def get_x_block_start_pos(self):
        return self.x_block_start_pos

def detect_chunk_with_position(block_position):
    return math.floor(block_position[0]/chunk_size[0])