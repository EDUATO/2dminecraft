import math

from files.terrain.chunk import Chunk
from files.blocks.Block import Block
from files.vars import chunk_size

def noisy_terrain(PerlinNoise:float, x, y, chunks_list:list, chunk_identifier:int):  
    blocks_to_gen = []
    r = noise_give_block(PerlinNoise)
    blocks_to_gen.append({"color":r, "y_coord":r, "noise":r})
    #print(blocks_to_gen)
    return blocks_to_gen

def noise_give_block(PerlinNoise):
    #print(PerlinNoise)
    to_ret = round(abs((PerlinNoise)))*10
    if to_ret > 255:
        return 255
    return to_ret

def get_blocks_chunks_list(index, chunks_list):
	return chunks_list[index].blocks