import pygame
import random

from files.terrain.noise import Noise
from files.vars import chunk_size
from files.terrain.chunk import Chunk
from files.terrain.noisy_terrain import noisy_terrain
from files.blocks.Block import Block


def reset_chunk_man_list():
	global chunk_manager_list
	chunk_manager_list = []

def initial_variables():
	global seed, Noise_gen, chunks_list, prw_noise, chunk_manager_list

	reset_chunk_man_list()

	seed = random.randint(-9999999, 9999999)
	Noise_gen = Noise(seed)

	chunks_list = []

	prw_noise = [1,1] # Previows noise

initial_variables()


def canGenerate(in_coords, chunk_identifier):
	global chunks_list
	# Fill the screen with air blocks, to define the blocks
	for chunk_ in chunks_list:
		if chunk_.Chunk_ID == chunk_identifier:
			return False
	return True

def generate(in_coords, time_s, chunk_identifier):
	# GENERATE AIR BLOCKS
	_canGenerate = canGenerate(in_coords, chunk_identifier=chunk_identifier)

	chunks_list.append(Chunk(id=chunk_identifier))
	blocks_to_gen = []
	if _canGenerate:
		# GENERATE TERRAIN
		x_chunk = chunk_size[0] * chunk_identifier
		
		prw_noise = [x_chunk, 1]
		
		for y in range(chunk_size[1]):
			y_pos = chunk_size[1] + y
			for x in range(chunk_size[0]):
				x_pos = x_chunk + x

				perlinHeight = Noise_gen.test(x_pos, y, chunk_size[1])
				gen_blocks = noisy_terrain(PerlinNoise=perlinHeight, y=chunk_size[1]-y, chunks_list=chunks_list, chunk_identifier=chunk_identifier)
				blocks_to_gen += gen_blocks

		chunks_list[len(chunks_list)-1].generate(blocks_list_to_generate=blocks_to_gen)
		print(f"[Generation] Chunk {chunk_manager_list[0]} generated!")

# Generation
def generation_loop():
	global chunk_manager_list
	for _ in range(len(chunk_manager_list)):
		if chunk_manager_list != []:
			generate((chunk_size[0] * chunk_manager_list[0]), 0, chunk_manager_list[0])
		
			chunk_manager_list.pop(0)
		else: break

			

		
			


