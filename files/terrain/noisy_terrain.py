import math, random

from files.blocks.Block import Block
from files.vars import chunk_size
from files.terrain.noise import Noise
from files.terrain.generation_variables import *


def noise_terrain_generator(chunk_identifier:int, NoiseGen:Noise)->list:
    """ The world generates each chunk from below to top and left to right """
    # GENERATE TERRAIN
    x_chunk = chunk_size[0] * chunk_identifier
    blocks_to_gen = []
    
    for y in range(chunk_size[1]):
        y_pos = chunk_size[1] + y
        
        for x in range(chunk_size[0]):
            x_pos = x_chunk + x

            perlinHeight = NoiseGen.test(x_pos, y, chunk_size[1])
            gen_blocks = noise_give_block(perlinHeight, y)
            blocks_to_gen.append( {"block":gen_blocks, "noise":perlinHeight} )

    blocks_to_gen = block_grass_check(blocks_to_gen)
    
    return blocks_to_gen

def noise_give_block(PerlinNoise, y):
    # Bedrock
    if y == 0:
        return 4
    
    if y <= PerlinNoise+20:
        return 2

    # Dirt
    if y < PerlinNoise + 27:
        return 3

    return 0

def block_grass_check(blocks_to_gen:list):
    """ Detect if an air block is after a dirt block and replace the dirt block with grass_block. """
    for i in range(len(blocks_to_gen)):
        if blocks_to_gen[i]['block'] == 3 and blocks_to_gen[i + chunk_size[0]]['block'] == 0:
            blocks_to_gen[i]['block'] = 1
            # Try to gen tree
            if tree_terrain_gen() == 7:
                blocks_to_gen[i]['block'] = 7

    return blocks_to_gen

def tree_terrain_gen( trees_margin=10):
    global tree_gen_margin
    if random.randint(0, 100) >= 80 and tree_gen_margin == 0:
        tree_gen_margin = 5
        return 7
    tree_gen_margin -= 1
    if tree_gen_margin < 0:
        tree_gen_margin = 0

def get_blocks_chunks_list(index, chunks_list):
	return chunks_list[index].blocks