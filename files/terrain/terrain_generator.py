import pygame
import random, time

from files.terrain.noise import Noise
from files.vars import chunk_size
from files.terrain.chunk import Chunk
from files.terrain.noisy_terrain import noise_terrain_generator
from files.blocks.Block import Block


def reset_chunk_man_list():
	global chunk_manager_list
	chunk_manager_list = []

def initial_variables():
	global seed, Noise_gen, chunks_list, chunk_manager_list

	reset_chunk_man_list()

	seed = random.randint(-9999999, 9999999)
	Noise_gen = Noise(seed)

	chunks_list = []

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
		blocks_to_gen = noise_terrain_generator(chunk_identifier, Noise_gen)
		chunks_list[len(chunks_list)-1].generate(blocks_list_to_generate=blocks_to_gen, time_sleep=time_s)
		#print(f"[Generation] Chunk {chunk_manager_list[0]} generated!")
		time.sleep(time_s)



# Generation
def generation_loop():
	global chunk_manager_list
	for _ in range(len(chunk_manager_list)):
		if chunk_manager_list != []:
			generate((chunk_size[0] * chunk_manager_list[0]), 0, chunk_manager_list[0])
		
			chunk_manager_list.pop(0)
		else: break


			

		
			


