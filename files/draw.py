import pygame
import random
import time
import threading

########## LOCAL MODULES ##########
from files.vars import Scene, win, modeX, modeY, block_scale_buff, block_to_put_id
import files.bucle as b
from files.import_imp import Blocks_texture
from files.fonts import *
import files.functions as f
from files.Block import Block, Blocks_list
from files.grid import grid

chunk_blocks_list = []
def generate(sleep):
	# Fill the screen with air blocks, to define the blocks
	for i in range(modeY// ( 16 * block_scale_buff )):
		for x in range(modeX//(16 * block_scale_buff)+1):
			chunk_blocks_list.append(Block(Blocks_texture, 0, [x,i])) 

	index = None
	# Grass floor
	for i in range(modeX//(16 * block_scale_buff)+1):
		
		if i == 0:
			# Find the grid position to start drawing 
			for f in range(len(chunk_blocks_list)):
				
				if chunk_blocks_list[f].getGridCoords()[1] == 8:
					index = f
					break

		chunk_blocks_list[index + (i)].setBlock(1)

	# Dirt level
	for i in range((modeX//(16 * block_scale_buff)+1) * 3):
		
		if i == 0:
			# Find the grid position to start drawing 
			for f in range(len(chunk_blocks_list)):
				
				if chunk_blocks_list[f].getGridCoords()[1] == 9:
					index = f
					break

		chunk_blocks_list[index + (i)].setBlock(3)

	# Stone level
	for i in range((modeX//(16 * block_scale_buff)+1) * 5):
		
		if i == 0:
			# Find the grid position to start drawing 
			for f in range(len(chunk_blocks_list)):
				
				if chunk_blocks_list[f].getGridCoords()[1] == 12:
					index = f
					break

		try:
			chunk_blocks_list[index + (i)].setBlock(2)
		except IndexError:
			pass

gen = threading.Thread(target=generate, args=[0.01])
gen.start()

selected_block = None
pygame.mouse.set_visible(False)

def Draw(events):
	global selected_block, block_to_put_id
	if Scene == 0:

		for i in range(len(chunk_blocks_list)):
			chunk_blocks_list[i].update()

		#grid(16, (0,0,100))

		pygame.draw.line(win, (255,255,255), (b.mouse_hitbox[0], 0), (b.mouse_hitbox[0], modeY))

		pygame.draw.line(win, (255,255,255), (0, b.mouse_hitbox[1]), (modeX, b.mouse_hitbox[1]))

		for i in range(len(chunk_blocks_list)):
			mouse_col_block = chunk_blocks_list[i].coordsInBlock(b.mouse_hitbox)

			if mouse_col_block:
				chunk_blocks_list[i].setglow(True)
				selected_block = chunk_blocks_list[i]
			else:
				chunk_blocks_list[i].setglow(False)

		try:
			# See if the selected_block is selected
			if not selected_block.isGlowing():
				selected_block = None

			
			# Clicks
			for event in events:
				if event.type == MOUSEBUTTONDOWN:
					if event.button == 1:
						selected_block.setBlock(0)
						
					elif event.button == 3:
						selected_block.setBlock(block_to_put_id)

					elif event.button == 4:
						if block_to_put_id >= len(Blocks_list)-1:
							block_to_put_id = 1
						else:
							block_to_put_id += 1

					elif event.button == 5:
						if block_to_put_id <= 1:
							block_to_put_id = len(Blocks_list)-1
						else:
							block_to_put_id -= 1

		except:
			pass

		f.text(str(b.fps), 0, 0, Arial_30, (255,255,255))
		f.text("Selected: " + str(Blocks_list[block_to_put_id]["Name"]), 400, 0, Arial_30, (255,255,255))