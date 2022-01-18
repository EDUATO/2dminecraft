import pygame
import random
import time

from files.noise import Noise
from files.Block import Block, Blocks_list
from files.import_imp import Blocks_texture

chunk_size = (16, 32)

seed = random.randint(1, 999999)
Noise_gen = Noise(seed)
test_noise = Noise_gen.test(10, 20)

chunk_blocks_list = []

con = 1

def airGen(in_coords):
	chunk_blocks_list.append([])
	
	# Fill the screen with air blocks, to define the blocks
	# Ordered : (0,0) , (1,0), (2,0), (3,0) *chunk_size[0]*, (0,1), (1,1), (2,1), ...
	for y in range( chunk_size[1] ):
		for x in range( chunk_size[0] ):
			POSITION = (x + in_coords,y)
			chunk_blocks_list[len(chunk_blocks_list)-1].append(
				{"POS":POSITION, "BLOCK":Block(Blocks_texture, 0, POSITION)}
				)

	#print(chunk_blocks_list[len(chunk_blocks_list)-1])

def generate(in_coords):
	# GENERATE AIR BLOCKS
	airGen(in_coords)
	
	# GENERATE TERRAIN
	a = 0
	for _ in range( chunk_size[1] ):
		
		for _ in range( chunk_size[0] ):
			
			if chunk_blocks_list[len(chunk_blocks_list)-1][a]["POS"][1] == 8:
				chunk_blocks_list[len(chunk_blocks_list)-1][a]["BLOCK"].setBlock(1)
				time.sleep(0.008)

			elif chunk_blocks_list[len(chunk_blocks_list)-1][a]["POS"][1] >= 9 and chunk_blocks_list[len(chunk_blocks_list)-1][a]["POS"][1] <= 13:
				chunk_blocks_list[len(chunk_blocks_list)-1][a]["BLOCK"].setBlock(3)
				time.sleep(0.008)
			
			elif chunk_blocks_list[len(chunk_blocks_list)-1][a]["POS"][1] >= 14 and chunk_blocks_list[len(chunk_blocks_list)-1][a]["POS"][1] <= chunk_size[1]-2:
				chunk_blocks_list[len(chunk_blocks_list)-1][a]["BLOCK"].setBlock(2)
				time.sleep(0.008)
			
			elif chunk_blocks_list[len(chunk_blocks_list)-1][a]["POS"][1] >= chunk_size[1]-1:
				chunk_blocks_list[len(chunk_blocks_list)-1][a]["BLOCK"].setBlock(5)
				time.sleep(0.008)
				

			a += 1


def find_coicidences(chunk_index, block_id):
	coincidences_list = []
	a = 0
	for _ in range( chunk_size[1] ):
		
		for _ in range( chunk_size[0] ):
			
			if chunk_blocks_list[chunk_index][a]["BLOCK"].getId() == block_id:
				coincidences_list.append(a)

			a += 1

	return coincidences_list


