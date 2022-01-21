import pygame
import random
import time
import math
import threading

from files.noise import Noise
from files.Block import Block, Blocks_list
from files.vars import chunk_size, Playing
from files.chunk import Chunk


seed = random.randint(1, 999999)
Noise_gen = Noise(seed)

chunks_list = []

con = 1

noise_sc = .1

prw_noise = [1,1]

def airGen(in_coords, Camera, chunk_identifier):
	global chunks_list
	chunk_blocks_list = []
	# Fill the screen with air blocks, to define the blocks
	# Ordered : (0,0) , (1,0), (2,0), (3,0) *chunk_size[0]*, (0,1), (1,1), (2,1), ...
	for y in range( chunk_size[1] ):
		for x in range( chunk_size[0] ):
			POSITION = (x + in_coords, y)
			chunk_blocks_list.append(
				{"POS":POSITION,
				"BLOCK":Block(ID=0, block_pos_grid=POSITION,Camera=Camera)}
				)
	# SINTAX : chunks_list[num]['BLOCKS'][list_num]['BLOCK'].method()
	chunks_list.append(
		{"CHUNK_DATA": Chunk(id=chunk_identifier, size=chunk_size, x_start_pos=in_coords),
		"BLOCKS":chunk_blocks_list}
	)
	
colors = [(0, 0, 0)]

for i in range(255):
	if not (i+1) > 255:
		colors.append( ((i+1), (i+1), (i+1)) )

def setBlock(chunk_id, block_index, block_id, noise_gen):
	chunks_list[chunk_id]["BLOCKS"][block_index]["BLOCK"].setBlock(block_id, noiseValue=noise_gen)

def generate(in_coords, time_s, Camera, chunk_identifier):
	global prw_noise
	# GENERATE AIR BLOCKS
	airGen(in_coords, Camera=Camera, chunk_identifier=chunk_identifier)
	
	# GENERATE TERRAIN
	block_index = 0
	y = 0
	chunk_id = chunk_identifier
	for y in range( chunk_size[1] ):
		for x in range( chunk_size[0] ):
			# GENERATE NOISE
			y_x = ( ((x) + prw_noise[0]), ((y) + prw_noise[1]) )
			formula = ((y_x[0]) * noise_sc, (y_x[1]) * noise_sc)
			
			noise_gen = Noise_gen.test( formula[0], formula[1] )
			
			# GENERATE TERRAIN

			# GRASS BLOCKS
			if (y == 10):
				setBlock(chunk_id=chunk_id, block_index=block_index, block_id=1, noise_gen=noise_gen)

			if (y < 10 ):
				setBlock(chunk_id=chunk_id, block_index=block_index, block_id=3, noise_gen=noise_gen)

			if (y < 9):
				if (noise_gen <= 0.1):
					setBlock(chunk_id=chunk_id, block_index=block_index, block_id=2, noise_gen=noise_gen)

				if (noise_gen >= 0.1):
					setBlock(chunk_id=chunk_id, block_index=block_index, block_id=3, noise_gen=noise_gen)

				if (noise_gen >= 0.7):
					setBlock(chunk_id=chunk_id, block_index=block_index, block_id=3, noise_gen=noise_gen)
			
				
			
			# BEDROCK
			if chunks_list[chunk_id]["BLOCKS"][block_index]["POS"][1] == 0:
				setBlock(chunk_id=chunk_id, block_index=block_index, block_id=5, noise_gen=noise_gen)
				chunks_list[chunk_id]["BLOCKS"][block_index]["BLOCK"].setBreakeable(False)
			
			block_index += 1

			

	# Save x and y to continue the noise in the next chunk		
	prw_noise[0] = x + prw_noise[0]

	prw_noise[1] = prw_noise[1]
	


def find_coicidences(chunk_index, block_id):
	coincidences_list = []
	block_index = 0
	for _ in range( chunk_size[1] ):
		
		for _ in range( chunk_size[0] ):
			
			if chunks_list[chunk_id]["BLOCKS"][block_index]["BLOCK"].getId() == block_id:
				coincidences_list.append(a)

			block_index += 1

	return coincidences_list

# Generation
def generation_loop(Camera):
	times = 0
	if Playing:
		for times in range(5):
			generate(chunk_size[0] * times, 0, Camera, times)
			print(f"[Generation] Chunk {times} generated!")

		print("[Generation] All chunks generated!")


