import pygame
import random
import time
import math
import threading

from files.Block import Block, Blocks_list
from files.vars import chunk_size, Playing
from files.chunk import Chunk
from files.functions import convert_camera_xy_to_block_pos
from files.chunk_generator import Chunk_Manager_List


seed = 10
#Noise_gen = Noise(seed)

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
		{"CHUNK_DATA": Chunk(id=chunk_identifier, size=chunk_size),
		"BLOCKS":chunk_blocks_list}
	)
	
colors = [(0, 0, 0)]

for i in range(255):
	if not (i+1) > 255:
		colors.append( ((i+1), (i+1), (i+1)) )

def get_blocks_chunks_list(index):
	return chunks_list[index]["BLOCKS"]

def gettBlockIndex(chunk_id, xy):
	blocks = get_blocks_chunks_list(index=len(chunks_list)-1)

	block_index = 0

	for s in range(len(blocks)):
		if blocks[s]["POS"] == xy:
			block_index = s
			break

	return block_index

def setBlock(chunk_id, block_index, block_id, noise_gen):
	blocks = get_blocks_chunks_list(index=len(chunks_list)-1)

	blocks[block_index]["BLOCK"].setBlock(block_id, noiseValue=noise_gen)

import noise

def generate(in_coords, time_s, Camera, chunk_identifier):
	# GENERATE AIR BLOCKS
	airGen(in_coords, Camera=Camera, chunk_identifier=chunk_identifier)
	
	# GENERATE TERRAIN
	y = 0
	chunk_id = chunk_identifier
	prw_noise = [1 + (15 * chunk_identifier), 1]

	# NEW #
	for x in range(chunk_size[0]):
		for y in range(chunk_size[1]):
			x_formula = in_coords + x
			y_formula = y
			block_index = gettBlockIndex(chunk_id, (x, y))


			""" Noise """
			y_x = ( ((x) + prw_noise[0]), ((y) + prw_noise[1]) )

			perlinHeight = int(noise.pnoise1(x=x_formula*0.5, octaves=3, persistence=1, lacunarity=3, repeat=99999999) * 5)

			blockIndex = gettBlockIndex(chunk_id=1, xy=(x, y))


			if get_blocks_chunks_list(index=len(chunks_list)-1)[block_index]["POS"][1] == 8 - perlinHeight:
				setBlock(chunk_id, block_index, 1, None)

			elif get_blocks_chunks_list(index=len(chunks_list)-1)[block_index]["POS"][1] < 8 - perlinHeight:
				setBlock(chunk_id, block_index, 3, None)

			if get_blocks_chunks_list(index=len(chunks_list)-1)[block_index]["POS"][1] < 8 - perlinHeight - 3:
				setBlock(chunk_id, block_index, 2, None)


			#setBlock(chunk_id=chunk_identifier, block_index=blockIndex, block_id=1, noise_gen=perlinHeight)

	
	print(chunk_identifier, "finished")

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
	if Chunk_Manager_List != []:
		for times in range(len(Chunk_Manager_List)):
			generate((chunk_size[0] * Chunk_Manager_List[0]), 0, Camera, Chunk_Manager_List[0])
			print(f"[Generation] Chunk {Chunk_Manager_List[0]} generated!")
			Chunk_Manager_List.pop(0)

			


