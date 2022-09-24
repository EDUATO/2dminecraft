import math, random

from files.blocks.Block import Block
from files.vars import chunk_size

def noisy_terrain(PerlinNoise:float, y, chunks_list:list, chunk_identifier:int):
    trees_margin = 0  
    blocks_to_gen = []
    b = noise_give_block(PerlinNoise, chunk_size[1]-y, trees_margin=trees_margin)
    blocks_to_gen.append({"block":b, "noise":PerlinNoise})
    trees_margin += 1
    #print(blocks_to_gen)
    return blocks_to_gen

def noise_give_block(PerlinNoise, y, trees_margin=0):
    if y == 0:
        return 4
    
    if y <= 20-int(PerlinNoise):
        return 2
    
    if y == 26-int(PerlinNoise):
        return 1
    elif y > 20-int(PerlinNoise) and y < 26-int(PerlinNoise):
        return 3

    # Trees test
    if y == 27-int(PerlinNoise) and trees_margin%21 == 0:
        r = random.randint(0,2)
        if r == 0:
            return 7

    return 0

def get_blocks_chunks_list(index, chunks_list):
	return chunks_list[index].blocks