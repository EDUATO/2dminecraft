import pygame
import random

from files.terrain.noise import Noise
from files.vars import chunk_size
from files.terrain.chunk import Chunk
#from files.terrain.chunk_generator import Chunk_Manager_List
from files.terrain.noisy_terrain import noisy_terrain



def reset_chunk_man_list():
	global Chunk_Manager_List
	Chunk_Manager_List = [0, 1, 2, 3, 4]

reset_chunk_man_list()

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


def airGen(in_coords, chunk_identifier):
	global chunks_list
	# Fill the screen with air blocks, to define the blocks
	chunks_list.append(Chunk(id=chunk_identifier))
	chunks_list[len(chunks_list)-1].generate()


def generate(in_coords, time_s, chunk_identifier):
	# GENERATE AIR BLOCKS
	airGen(in_coords, chunk_identifier=chunk_identifier)
	
	# GENERATE TERRAIN
	y = 0
	x = 0
	chunk_id = chunk_identifier
	prw_noise = [(chunk_size[0] * chunk_identifier), 1]

	# NEW #
	for x in range(chunk_size[0]):
		y_x = ( ((x) + prw_noise[0]), ((seed) + prw_noise[1]) )

		perlinHeight = Noise_gen.test(y_x[0], seed, chunk_size[1])
		for y in range(chunk_size[1]):
			noisy_terrain(PerlinNoise=perlinHeight, y_x=y_x, y=y, chunks_list=chunks_list, chunk_identifier=chunk_id)

# Generation
def generation_loop():
	global Chunk_Manager_List
	print("Ha")
	#initial_variables()
	if Chunk_Manager_List != []:
		for times in range(len(Chunk_Manager_List)):
			generate((chunk_size[0] * Chunk_Manager_List[0]), 0, Chunk_Manager_List[0])
			print(f"[Generation] Chunk {Chunk_Manager_List[0]} generated!")
			Chunk_Manager_List.pop(0)

		
			


