import pygame
import random
import time
import math
import threading

from files.noise import Noise
from files.Block import Block, Blocks_list
from files.vars import chunk_size, Playing


seed = random.randint(1, 999999)
Noise_gen = Noise(seed)

chunk_blocks_list = []

con = 1

noise_sc = .1

prw_noise = [1,1]

def airGen(in_coords, Camera):
	chunk_blocks_list.append([])
	
	# Fill the screen with air blocks, to define the blocks
	# Ordered : (0,0) , (1,0), (2,0), (3,0) *chunk_size[0]*, (0,1), (1,1), (2,1), ...
	for y in range( chunk_size[1] ):
		for x in range( chunk_size[0] ):
			POSITION = (x + in_coords, y)
			chunk_blocks_list[len(chunk_blocks_list)-1].append(
				{"POS":POSITION,
				"BLOCK":Block(ID=0, block_pos_grid=POSITION,Camera=Camera)}
				)

	#print(chunk_blocks_list[len(chunk_blocks_list)-1])

colors = [(0, 0, 0)]

for i in range(255):
	if not (i+1) > 255:
		colors.append( ((i+1), (i+1), (i+1)) )

def generate(in_coords, time_s, Camera):
	global prw_noise
	# GENERATE AIR BLOCKS
	airGen(in_coords, Camera=Camera)
	
	# GENERATE TERRAIN
	a = 0
	y = 0
	for y in range( chunk_size[1] ):
		for x in range( chunk_size[0] ):
			# GENERATE NOISE
			y_x = ( ((x) + prw_noise[0]), ((y) + prw_noise[1]) )
			formula = ((y_x[0]) * noise_sc, (y_x[1]) * noise_sc)
			
			noise_gen = Noise_gen.test( formula[0], formula[1] )
			
			# GENERATE TERRAIN

			# GRASS BLOCKS
			if (y == 10):
				chunk_blocks_list[len(chunk_blocks_list)-1][a]["BLOCK"].setBlock(1, noiseValue=noise_gen)

			if (y < 10 ):
				chunk_blocks_list[len(chunk_blocks_list)-1][a]["BLOCK"].setBlock(3, noiseValue=noise_gen)

			if (y < 9):
				if (noise_gen <= 0.1):
					chunk_blocks_list[len(chunk_blocks_list)-1][a]["BLOCK"].setBlock(2, noiseValue=noise_gen)

				if (noise_gen >= 0.1):
					chunk_blocks_list[len(chunk_blocks_list)-1][a]["BLOCK"].setBlock(3, noiseValue=noise_gen)

				if (noise_gen >= 0.7):
					chunk_blocks_list[len(chunk_blocks_list)-1][a]["BLOCK"].setBlock(3, noiseValue=noise_gen)

			
				
			
			# BEDROCK
			if chunk_blocks_list[len(chunk_blocks_list)-1][a]["POS"][1] == 0:
				chunk_blocks_list[len(chunk_blocks_list)-1][a]["BLOCK"].setBlock(5, noiseValue=noise_gen)
				chunk_blocks_list[len(chunk_blocks_list)-1][a]["BLOCK"].setBreakeable(False)


			a += 1

			

	# Save x and y to continue the noise in the next chunk		
	prw_noise[0] = x + prw_noise[0]

	prw_noise[1] = prw_noise[1]
	


def find_coicidences(chunk_index, block_id):
	coincidences_list = []
	a = 0
	for _ in range( chunk_size[1] ):
		
		for _ in range( chunk_size[0] ):
			
			if chunk_blocks_list[chunk_index][a]["BLOCK"].getId() == block_id:
				coincidences_list.append(a)

			a += 1

	return coincidences_list

# Generation
def generation_loop(Camera):
	times = 0
	if Playing:
		for times in range(3):
			generate(chunk_size[0] * times, 0, Camera)
			print(f"[Generation] Chunk {times} generated!")

		print("[Generation] All chunks generated!")


