import pygame
import random
import time
import threading
import math

########## LOCAL MODULES ##########
from files.vars import Scene, win, modeX, modeY, block_scale_buff, block_to_put_id, Playing, camera_coords
import files.bucle as b
from files.import_imp import Blocks_texture, Player_texture
from files.fonts import *
import files.functions as f
from files.Block import Block, Blocks_list
from files.grid import grid
from files.player import Player
from files.terrain_generator import generate, chunk_blocks_list, seed, chunk_size

# Generation
def generation_loop():
	times = 0
	if Playing:
		for times in range(10):
			generate(16 * times)
			print(f"Chunk {times} generated!")

loop = threading.Thread(target=generation_loop, daemon=True) # It destroy when the main thread ends
loop.start()

p1 = Player(Player_texture, ("m", 200))

selected_block = None
pygame.mouse.set_visible(False)

ActiveChunks = [chunk_blocks_list[0]]


def Draw(events):
	global selected_block, block_to_put_id, ActiveChunks
	if Scene == 0:
		# CHUNCK VIEW
		for c in range(len(chunk_blocks_list)):

			for n in range(len(chunk_blocks_list)):
				chunk_initial_place = (chunk_size[0] * (16 * block_scale_buff) * (n))
				chunk_real_size = (chunk_size[0] * (16 * block_scale_buff) * (n+1)) # 16 is the block size
				if p1.get_pos()[0] - camera_coords[0] > chunk_initial_place and p1.get_pos()[0] - camera_coords[0] < chunk_real_size+1:
					break

			try:
				ActiveChunks = [chunk_blocks_list[n-1], chunk_blocks_list[n], chunk_blocks_list[n+1]]
			except:
				try:
					ActiveChunks = [chunk_blocks_list[n-1], chunk_blocks_list[n]]
				except:
					ActiveChunks = [chunk_blocks_list[n]]
		# UPDATE ACTIVECHUNKS
		try:
			for c in range(len(ActiveChunks)):
				for i in range(len(ActiveChunks[c])):
					ActiveChunks[c][i]["BLOCK"].update()
		except:
			pass

		#grid(16, (0,0,100))

		pygame.draw.line(win, (255,255,255), (b.mouse_hitbox[0], 0), (b.mouse_hitbox[0], modeY))

		pygame.draw.line(win, (255,255,255), (0, b.mouse_hitbox[1]), (modeX, b.mouse_hitbox[1]))
		try:
			for c in range(len(ActiveChunks)):
				for i in range(len(ActiveChunks[c])):
					mouse_col_block = ActiveChunks[c][i]["BLOCK"].coordsInBlock(b.mouse_hitbox)

					if mouse_col_block:
						ActiveChunks[c][i]["BLOCK"].setglow(True)

						selected_block = ActiveChunks[c][i]

					else:
						ActiveChunks[c][i]["BLOCK"].setglow(False)
		except:
			pass
		try:
			# See if the selected_block is selected
			if not selected_block["BLOCK"].isGlowing():
				selected_block = None

			
			# Clicks
			for event in events:
				if event.type == MOUSEBUTTONDOWN:
					if event.button == 1:
						selected_block["BLOCK"].setBlock(0)
						print(selected_block["POS"])
						
					elif event.button == 3:
						selected_block["BLOCK"].setBlock(block_to_put_id)
						print(selected_block["POS"])

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

		
		p1.update()
		p1.move(events)
		
		

		# Blocks touching
		
		"""
		p1_hitbox = p1.get_hitbox()
		for c in range(len(chunk_blocks_list)):
			for i in range(len(chunk_blocks_list[c])):
				to = chunk_blocks_list[c][i]["BLOCK"].coll_hitbox(p1_hitbox)

				if to:
					chunk_blocks_list[c][i]["BLOCK"].setglow(True)
					to = False"""

		f.text("Terrain seed: " + str(seed), modeX-400, 0, Arial_30, (255,255,255))
		f.text(str(b.fps), 0, 0, Arial_30, (255,255,255))
		f.text("Selected: " + str(Blocks_list[block_to_put_id]["Name"]), 400, 0, Arial_30, (255,255,255))