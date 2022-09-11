import pygame
import random

from files.terrain.noise import Noise
from files.vars import chunk_size
from files.terrain.chunk import Chunk
from files.terrain.noisy_terrain import noisy_terrain



def reset_chunk_man_list():
	global Chunk_Manager_List
	Chunk_Manager_List = [0]

def initial_variables():
	global seed, Noise_gen, chunks_list, con, noise_sc, prw_noise, Chunk_Manager_List

	reset_chunk_man_list()

	seed = 10
	Noise_gen = Noise(seed)

	chunks_list = []

	con = 1

	noise_sc = .1

	prw_noise = [1,1] #Previows noise

initial_variables()


def canGenerate(in_coords, chunk_identifier):
	global chunks_list
	# Fill the screen with air blocks, to define the blocks
	for chunk_ in chunks_list:
		if chunk_.Chunk_ID == chunk_identifier:
			return False

	"""chunks_list.append(Chunk(id=chunk_identifier))
	chunks_list[len(chunks_list)-1].generate()
"""
	return True

def generate(in_coords, time_s, chunk_identifier):
	# GENERATE AIR BLOCKS
	_canGenerate = canGenerate(in_coords, chunk_identifier=chunk_identifier)
	chunks_list.append(Chunk(id=chunk_identifier))
	blocks_to_gen = []

	if _canGenerate:
		#print(f"generating {chunk_identifier}")
		# GENERATE TERRAIN
		y = 0
		x = 0
		x_chunk = chunk_size[0] * chunk_identifier
		
		prw_noise = [x_chunk, 1]
		
		for y in range(chunk_size[1]):
			y_pos = chunk_size[1] + y
			for x in range(chunk_size[0]):
				x_pos = x_chunk + x

				perlinHeight = Noise_gen.test(x_pos, y_pos, chunk_size[1])
				gen_blocks = noisy_terrain(PerlinNoise=perlinHeight, x=x_pos, y=y, chunks_list=chunks_list, chunk_identifier=chunk_identifier)
				blocks_to_gen += gen_blocks

		chunks_list[len(chunks_list)-1].generate(blocks_list_to_generate=blocks_to_gen)

# Generation
def generation_loop():
	global Chunk_Manager_List
	if Chunk_Manager_List != []:
		for times in range(len(Chunk_Manager_List)):
			generate((chunk_size[0] * Chunk_Manager_List[0]), 0, Chunk_Manager_List[0])
			try:
				#print(f"[Generation] Chunk {Chunk_Manager_List[0]} generated!")
				Chunk_Manager_List.pop(0)
			except IndexError: pass
			

		
			


