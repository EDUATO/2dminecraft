import math

from files.terrain.chunk import Chunk
from files.blocks.Block import Block
from files.vars import chunk_size

def noisy_terrain(PerlinNoise:float, y, chunks_list:list, chunk_identifier:int):  
    blocks_to_gen = []
    b = noise_give_block(PerlinNoise, chunk_size[1]-y)
    blocks_to_gen.append({"block":b, "noise":PerlinNoise})
    #print(blocks_to_gen)
    return blocks_to_gen

def noise_give_block(PerlinNoise, y):
    if y == 0:
        return 4
    
    if y <= 20-int(PerlinNoise):
        return 2
    
    if y == 26-int(PerlinNoise):
        return 1
    elif y > 20-int(PerlinNoise) and y < 26-int(PerlinNoise):
        return 3

    return 0

def get_blocks_chunks_list(index, chunks_list):
	return chunks_list[index].blocks