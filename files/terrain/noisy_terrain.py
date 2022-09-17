import math

from files.terrain.chunk import Chunk
from files.blocks.Block import Block
from files.vars import chunk_size

def noisy_terrain(PerlinNoise:float, y, chunks_list:list, chunk_identifier:int):  
    blocks_to_gen = []
    b = noise_give_block(PerlinNoise, y)
    blocks_to_gen.append({"block":b, "noise":PerlinNoise})
    #print(blocks_to_gen)
    return blocks_to_gen

def noise_give_block(PerlinNoise, y):
    if y > 45 - int(PerlinNoise):
        return 2
    if y == 41-int(PerlinNoise):
        return 1
    if y > 41-int(PerlinNoise) and y <= 45 - int(PerlinNoise):
        return 3

    return 0

def get_blocks_chunks_list(index, chunks_list):
	return chunks_list[index].blocks