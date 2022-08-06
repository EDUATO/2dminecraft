import pygame
import random
import time
import math
import threading

from files.terrain.noise import Noise
from files.blocks.Block import Block, every_block_list
from files.vars import chunk_size, Playing
from files.terrain.chunk import Chunk
from files.functions import convert_camera_xy_to_block_pos
from files.terrain.chunk_generator import Chunk_Manager_List
from files.terrain.noisy_terrain import noisy_terrain


seed = 10
Noise_gen = Noise(seed)

chunks_list = []

con = 1

noise_sc = .1

prw_noise = [1,1]

owo = []

def airGen(in_coords, chunk_identifier):
	global chunks_list, owo
	chunk_blocks_list = []
	# Fill the screen with air blocks, to define the blocks
	# Ordered : (0,0) , (1,0), (2,0), (3,0) *chunk_size[0]*, (0,1), (1,1), (2,1), ...
	for y in range( chunk_size[1] ):
		for x in range( chunk_size[0] ):
			POSITION = (x + in_coords, y)
			chunk_blocks_list.append(
				Block(block_pos_grid=POSITION)
				)
	"""for i in chunk_blocks_list:
		i.setBlock(1)"""
	
	# SINTAX : chunks_list[num]['BLOCKS'][block_num].block_method()
	chunks_list.append(
		{"CHUNK_DATA": Chunk(id=chunk_identifier, size=chunk_size),
		"BLOCKS":chunk_blocks_list}
	)

	owo.append(
		{"CHUNK_DATA": Chunk(id=chunk_identifier, size=chunk_size),
		"BLOCKS":chunk_blocks_list}
	)
	
colors = [(0, 0, 0)]

for i in range(255):
	if not (i+1) > 255:
		colors.append( ((i+1), (i+1), (i+1)) )


def generate(in_coords, time_s, chunk_identifier):
	# GENERATE AIR BLOCKS
	airGen(in_coords, chunk_identifier=chunk_identifier)
	
	"""# GENERATE TERRAIN
	y = 0
	x = 0
	chunk_id = chunk_identifier
	prw_noise = [(chunk_size[0] * chunk_identifier), 1]

	# NEW #
	for x in range(chunk_size[0]):
		y_x = ( ((x) + prw_noise[0]), ((seed) + prw_noise[1]) )

		perlinHeight = Noise_gen.test(y_x[0], seed, chunk_size[1])
		for y in range(chunk_size[1]):
			noisy_terrain(PerlinNoise=perlinHeight, y_x=y_x, y=y, chunks_list=chunks_list, chunk_identifier=chunk_id)"""


def find_coicidences(chunk_index, block_id):
	coincidences_list = []
	block_index = 0
	for _ in range( chunk_size[1] ):
		
		for _ in range( chunk_size[0] ):
			
			if chunks_list[chunk_id]["BLOCKS"][block_index].getId() == block_id:
				coincidences_list.append(a)

			block_index += 1

	return coincidences_list

# Generation
def generation_loop():
	if Chunk_Manager_List != []:
		for times in range(len(Chunk_Manager_List)):
			generate((chunk_size[0] * Chunk_Manager_List[0]), 0, Chunk_Manager_List[0])
			print(f"[Generation] Chunk {Chunk_Manager_List[0]} generated!")
			Chunk_Manager_List.pop(0)

			


