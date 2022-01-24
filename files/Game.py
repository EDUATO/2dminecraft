import pygame
import random
import time
import threading
import math

########## LOCAL MODULES ##########
from files.vars import Scene, block_scale_buff, Playing, DebugScreen, block_size, chunk_size, block_to_put_id, modeY, Pause
import files.bucle as b
from files.fonts import *
import files.functions as f
from files.Block import Blocks_list
from files.grid import grid
import files.gui.gui_class as gui

from files.classes_init import * # All the classes/methods will be initialized here

lastChunkID = "None"
inChunkID = "None"

def game(events, surface):
	global selected_block, block_to_put_id, ActiveChunks, inChunkID, lastChunkID
	inGameEvents(events)
	Entity_hitbox = p1.get_hitbox()

	ActiveChunks = []
	for ch in range(len(chunks_list)):
		ChunkID = chunks_list[ch]["CHUNK_DATA"].isRectInChunk(surface=surface, camera=CameraMain, Rect=pygame.Rect(Entity_hitbox))


		if ChunkID:
			if not ch == 0:
				ActiveChunks.append(chunks_list[ch-1])
			ActiveChunks.append(chunks_list[ch])
			try:
				ActiveChunks.append(chunks_list[ch+1])
			except IndexError:
				pass


			if inChunkID == "None":
				inChunkID = chunks_list[ch]["CHUNK_DATA"].get_chunk_id()
				lastChunkID = inChunkID
			else:
				lastChunkID = inChunkID
				inChunkID = chunks_list[ch]["CHUNK_DATA"].get_chunk_id()
			break

	# UPDATE ACTIVECHUNKS
	for c in range(len(ActiveChunks)):
		for i in range(len(ActiveChunks[c]["BLOCKS"])):
			ActiveChunks[c]["BLOCKS"][i]["BLOCK"].update(deltaTime=b.deltaTime, surface=surface, Camera=CameraMain)
			ActiveChunks[c]["BLOCKS"][i]["BLOCK"].set_light_val(value=200)

		

	for c in range(len(ActiveChunks)):
		ActiveChunks[c]["CHUNK_DATA"].DrawChunkLimits(surface=surface, camera=CameraMain)

		
		


	### MOUSE CONTROLLER ###
	camera_size = CameraMain.get_camera_size()

	if not (gui.inGui or Pause):
		# Cursor
		pygame.draw.line(surface, (255,255,255), (b.mouse_hitbox[0], 0), (b.mouse_hitbox[0], camera_size[1]))
		pygame.draw.line(surface, (255,255,255), (0, b.mouse_hitbox[1]), (camera_size[0], b.mouse_hitbox[1]))

		p1.keyMovement() # Be able to move the player

	for c in range(len(ActiveChunks)):
		for i in range(len(ActiveChunks[c]["BLOCKS"])):
			if not (gui.inGui or Pause) :
				# Detect a block being touched by the cursor
				mouse_col_block = ActiveChunks[c]["BLOCKS"][i]["BLOCK"].coll_hitbox2(b.mouse_hitbox)
				if mouse_col_block:
					selected_block = ActiveChunks[c]["BLOCKS"][i]
					selected_block["BLOCK"].setglow(True)
					
				else:
					ActiveChunks[c]["BLOCKS"][i]["BLOCK"].resetBreakState() # Reset break state
					ActiveChunks[c]["BLOCKS"][i]["BLOCK"].setglow(False)
			else:
				ActiveChunks[c]["BLOCKS"][i]["BLOCK"].setglow(False)

	global p1_pos
	p1_pos = p1.get_camera_pos()

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
		if not (gui.inGui or Pause):
			if mouse[0]:
				selected_block["BLOCK"].breakBlock(surface=surface, id=0)
			else:
				selected_block["BLOCK"].resetBreakState()
		else:
			selected_block["BLOCK"].resetBreakState()
			
		if mouse[2]:
			if not (gui.inGui or Pause):
				if not block_to_put_id == None:
					if selected_block["BLOCK"].getId() == 0:
						if keys[K_LALT] == 1:
							selected_block["BLOCK"].setBlock(block_to_put_id, background=True)
						else:
							selected_block["BLOCK"].setBlock(block_to_put_id, background=False)


	except TypeError:
		pass

	# Player
	p1.update(surface=surface, chunks_list=ActiveChunks, deltaTime=b.deltaTime, camera=CameraMain)

	# Update entities
	for i in range(len(EntitiesInGame)):
		EntitiesInGame[i].update(surface=surface, chunks_list=ActiveChunks, deltaTime=b.deltaTime, camera=CameraMain)

	Player_Hotbar.update(events, surface)

	PlayerInventory.update(surface, b.mouse_hitbox, keys)

	Debugging_Screen(surface=surface, selected_block=selected_block)

	# FOCUS CAMERA
	pe =  f.convert_blocks_pos_to_camera_xy(p1.get_block_pos())
	CameraMain.set_x_coord(value=(pe[0] + CameraMain.get_camera_size()[0]//2))
	CameraMain.set_y_coord(value=(pe[1] + CameraMain.get_camera_size()[1]//2 - 100))
	
	

	# TEST ONLY
	for event in events:
		
		if event.type == pygame.KEYDOWN:
			if event.key == K_t:
				ch = f.convert_blocks_pos_to_camera_xy(grid_pos=selected_block["BLOCK"].getGridCoords())	

				CameraMain.set_x_coord(ch[0])
				CameraMain.set_y_coord(ch[1])

	vel = 5
	keys = pygame.key.get_pressed()
	

	if keys[K_RIGHT]:
		CameraMain.set_x_coord(-vel,addToTheVar=True)

	if keys[K_LEFT]:
		CameraMain.set_x_coord(vel,addToTheVar=True)

	if keys[K_UP]:
		CameraMain.set_y_coord(vel,addToTheVar=True)

	if keys[K_DOWN]:
		CameraMain.set_y_coord(-vel,addToTheVar=True)

	if Pause:
		pygame.mouse.set_visible(True)

def Debugging_Screen(surface, selected_block):
	""" It shows some variables that may be useful to test """

	player_pos_in_blocks = f.convert_camera_xy_to_block_pos(xy_pos=( (p1_pos[0], p1_pos[1]) ))


	if DebugScreen:
		debug_screen.addDebugText(text=f"FPS: {round(b.fps.get_fps())}", color=(200,0,0))
		
		debug_screen.addDebugText(text=f"Terrain seed: {seed}", color=(255,255,255))

		debug_screen.addDebugText(text=f"PLAYER POS: {round(player_pos_in_blocks[0], 3)}, {round(player_pos_in_blocks[1], 3)}", color=(0,200,0))

		debug_screen.addDebugText(text=f"IN CHUNK: {inChunkID}", color=(0,200,0))

		debug_screen.addDebugText(text=f"PLAYER POS2: {round(p1_pos[0], 3)}, {round(p1_pos[1], 3)}", color=(0,200,0))

		

		if selected_block != None: 

			debug_screen.addDebugText(text=f"Noise Value: {selected_block['BLOCK'].getNoiseValue()}", color=(255,255,255))

			#debug_screen.addDebugText(text=f"isBackground: {selected_block['BLOCK'].isBackground()}", color=(255,255,255))

			#debug_screen.addDebugText(text=f"{selected_block['BLOCK'].getBreakPorcentage()} %", color=(255,255,255))

		debug_screen.addDebugText(text=f"CAMERA MAIN: {round(CameraMain.get_xy()[0],2), round(CameraMain.get_xy()[1],2)}", color=(0,0,200))

		debug_screen.addDebugText(text=f"CAMERA MAIN COORDS: {a}", color=(0,200,0))
		

		debug_screen.Show(surface)

		debug_screen.resetDebugList()
		

	


def inGameEvents(events):
	global DebugScreen, Pause
	
	for event in events:
		if event.type == pygame.KEYDOWN:
			if event.key == K_F3:
				if not Pause:
					if DebugScreen:
						DebugScreen = False
					else:
						DebugScreen = True

			elif event.key == K_ESCAPE:
				if not gui.inGui:
					if Pause:
						Pause = False
					else:
						Pause = True

		elif event.type == pygame.WINDOWMOVED:
			Pause = True

		elif event.type == pygame.WINDOWMINIMIZED:
			Pause = True