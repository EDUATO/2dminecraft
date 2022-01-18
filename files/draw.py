import pygame
import random
import time
import threading
import math

########## LOCAL MODULES ##########
from files.vars import Scene, win, modeX, modeY, block_scale_buff, Playing, camera_coords, DebugScreen, block_size, chunk_size, block_to_put_id
import files.bucle as b
from files.import_imp import Blocks_texture, Player_texture
from files.fonts import *
import files.functions as f
from files.Block import Block, Blocks_list
from files.grid import grid
from files.player import Player
from files.terrain_generator import generate, chunk_blocks_list, seed
from files.gui.Inventory import Inventory, PlayerInventory
from files.gui.gui_class import inGui
from files.gui.hotbar import Hotbar

# Generation
def generation_loop():
	times = 0
	if Playing:
		for times in range(16):
			generate(chunk_size[0] * times)
			print(f"[Generation] Chunk {times} generated!")

		print("[Generation] All chunks generated!")

loop = threading.Thread(target=generation_loop, daemon=True) # It destroy when the main thread ends
loop.start()

p1 = Player(Player_texture, ("m", 193))

selected_block = None

ActiveChunks = [chunk_blocks_list[0]]

pygame.mouse.set_visible(False) # Hide cursor

Player_Hotbar = Hotbar()

def Draw(events):
	global selected_block, block_to_put_id, ActiveChunks
	if Scene == 0:
		# CHUNCK VIEW
		for c in range(len(chunk_blocks_list)):

			for n in range(len(chunk_blocks_list[c])):
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
					try:
						ActiveChunks = [chunk_blocks_list[n]]
					except:
						pass
			break
		# UPDATE ACTIVECHUNKS
		for c in range(len(ActiveChunks)):
			for i in range(len(ActiveChunks[c])):
				ActiveChunks[c][i]["BLOCK"].update(deltaTime=b.deltaTime)

		

		# Mouse
		if inGui == False:
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
							ActiveChunks[c][i]["BLOCK"].resetBreakState() # Reset break state
							ActiveChunks[c][i]["BLOCK"].setglow(False)
			except:
				pass

		# Player
		p1.update(ActiveChunks, deltaTime=b.deltaTime)
		p1.keyMovement()

		keys = pygame.key.get_pressed()
		mouse = pygame.mouse.get_pressed()

		try:
			# Get block id
			block_to_put_id = Player_Hotbar.get_slot_item()["Item"][0]
		except:
			block_to_put_id = None

		try:
			# See if the selected_block is selected
			if not selected_block["BLOCK"].isGlowing():
				selected_block = None

			
			# Clicks
			if mouse[0]:
				selected_block["BLOCK"].breakBlock(0)
				print(selected_block["POS"])
			else:
				selected_block["BLOCK"].resetBreakState()
				
			if mouse[2]:
				if not block_to_put_id == None:
					if selected_block["BLOCK"].getId() == 0:
						if keys[K_LALT] == 1:
							selected_block["BLOCK"].setBlock(block_to_put_id, background=True)
						else:
							selected_block["BLOCK"].setBlock(block_to_put_id)


		except TypeError:
			pass
		
		Player_Hotbar.update(events)

		PlayerInventory.update(b.mouse_hitbox, keys)

		if DebugScreen:
			f.text("Terrain seed: " + str(seed), modeX-400, 0, Arial_30, (255,255,255))
			f.text(str(b.fps), 0, 0, Arial_30, (255,255,255))
			

			try:
				f.text("Noise Value: " + str(selected_block["BLOCK"].getNoiseValue()) , 400, 50, Arial_30, (255,255,255))
			except:
				f.text("Noise Value: None" , 400, 50, Arial_30, (255,255,255))


			try:
				f.text("isBackground : " + str(selected_block["BLOCK"].isBackground()), 0, 50, Arial_30, (255,255,255))
			except:
				pass

			try:
				f.text(str(selected_block["BLOCK"].getBreakPorcentage()) + "%", 250, 50, Arial_30, (255,255,255))
			except:
				pass

			grid(block_size, (0,0,100))