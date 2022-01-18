import pygame
import random
import time
import math

from files.noise import Noise
from files.Block import Block, Blocks_list
from files.import_imp import Blocks_texture

chunk_size = (16, 32)

seed = random.randint(1, 999999)
Noise_gen = Noise(seed)

chunk_blocks_list = []

con = 1

noise_sc = .1

prw_noise = [1,1]

def airGen(in_coords):
	chunk_blocks_list.append([])
	
	# Fill the screen with air blocks, to define the blocks
	# Ordered : (0,0) , (1,0), (2,0), (3,0) *chunk_size[0]*, (0,1), (1,1), (2,1), ...
	for y in range( chunk_size[1] ):
		for x in range( chunk_size[0] ):
			POSITION = (x + in_coords, chunk_size[1] - y)
			chunk_blocks_list[len(chunk_blocks_list)-1].append(
				{"POS":POSITION, "BLOCK":Block(Blocks_texture, 0, POSITION)}
				)

	#print(chunk_blocks_list[len(chunk_blocks_list)-1])

colors = [(0, 0, 0)]

for i in range(255):
	if not (i+1) > 255:
		colors.append( ((i+1), (i+1), (i+1)) )

def generate(in_coords):
	global prw_noise
	# GENERATE AIR BLOCKS
	airGen(in_coords)
	
	# GENERATE TERRAIN
	a = 0
	y = 0
	for y in range( chunk_size[1] ):
		for x in range( chunk_size[0] ):
			
			#noise_a = Noise_gen.test( noi[0], noi[1])
			#print("Noise " + str(noise_a))
			"""
			if (noise_a <= 0.2):
				if chunk_blocks_list[len(chunk_blocks_list)-1][a]["POS"][1] >= 6:
					chunk_blocks_list[len(chunk_blocks_list)-1][a]["BLOCK"].setBlock(2)
					time.sleep(0.000001)

			if (noise_a >= 0.2):
				if chunk_blocks_list[len(chunk_blocks_list)-1][a]["POS"][1] >= 6:
					chunk_blocks_list[len(chunk_blocks_list)-1][a]["BLOCK"].setBlock(3)
					time.sleep(0.000001)

			if (noise_a >= 0.4):
				if chunk_blocks_list[len(chunk_blocks_list)-1][a]["POS"][1] >= 6:
					chunk_blocks_list[len(chunk_blocks_list)-1][a]["BLOCK"].setBlock(4)
					time.sleep(0.000001)

			if (noise_a >= 0.7):
				if chunk_blocks_list[len(chunk_blocks_list)-1][a]["POS"][1] >= 6:
					chunk_blocks_list[len(chunk_blocks_list)-1][a]["BLOCK"].setBlock(5)
					time.sleep(0.000001)"""

			y_x = ( ((x) + prw_noise[0]), ((y) + prw_noise[1]) )
			formula2 = ((y_x[0]) * noise_sc, (y_x[1]) * noise_sc)
			


			noise_gen = Noise_gen.test( formula2[0], formula2[1] )
			if (255 * noise_gen > 255):
				chunk_blocks_list[len(chunk_blocks_list)-1][a]["BLOCK"].setBlock(0, color=(0,0,0, 255))
			elif (255 * noise_gen < 0):
				chunk_blocks_list[len(chunk_blocks_list)-1][a]["BLOCK"].setBlock(0, color=(0,0,0, 0))
			else:
				chunk_blocks_list[len(chunk_blocks_list)-1][a]["BLOCK"].setBlock(0, color=(0,0,0, 255.0 * noise_gen ))

			
			if y == 0 and x ==  0:
				print("CHUNK ID: " + str(len(chunk_blocks_list)-1))
				print("START")
				print("Y = 0")
				print(str((y_x[0])) + " - " + str((y_x[1])))
				print("---------")
			if y == chunk_size[1] and x ==  chunk_size[0]:
				print("CHUNK ID: " + str(len(chunk_blocks_list)-1))
				print("Y = chunk_size[1]")
				print(str((y_x[0])) + " - " + str((y_x[1])))
				print("END")
				print("---------")
				print("x-x-x-x---x")

			if y == 0:
				print("TEST_ Y = 0")
				print("CHUNK ID: " + str(len(chunk_blocks_list)-1))
				print(str((y_x[0])) + " - " + str((y_x[1])))
				



			# BEDROCK
			if chunk_blocks_list[len(chunk_blocks_list)-1][a]["POS"][1] == 6:
				chunk_blocks_list[len(chunk_blocks_list)-1][a]["BLOCK"].setBlock(5)
				#chunk_blocks_list[len(chunk_blocks_list)-1][a]["BLOCK"].setBreakeable(False)


			# Grass
			"""if chunk_blocks_list[len(chunk_blocks_list)-1][a]["POS"][1] == noise_a:
				
				chunk_blocks_list[len(chunk_blocks_list)-1][a]["BLOCK"].setBlock(1)
				time.sleep(0.008)"""
				
			#print(str(prw_noise[0])  + " - " + str(prw_noise[1]))
			
			a += 1

			
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


