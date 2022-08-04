import pygame
import random
import time
import threading
import math

########## LOCAL MODULES ##########
from files.vars import Scene, block_scale_buff, Playing, DebugScreen, block_size, chunk_size, block_to_put_id, modeY
import files.bucle as b
from files.fonts import *
import files.functions as f
from files.blocks.Block import every_block_list
from files.grid import grid
import files.gui.gui_class as gui
from files.blocks.block_data import placeble_blocks_list
from files.entity.player_mouse_controller import player_mouse_cotroller
from files.gui.pauseMenu import PauseMenu
from files.saving.gamesave import save

from files.classes_init import * # Game's classes and vars initialization

class Game(Game_Initialization):
	def __init__(self):
		super().__init__()

		self.init_blocks()

		self.LastLoadedChunkId = 0

		self.lastChunkID = "None"

		self.foc = True

		self.Pause = False

	def update(self, events, surface):
		if self.full_initialation:
			self.classes = self.Entities_man.getEntitiesClasses()
			# Clear screen
			surface.fill((154,203,255))

			self.update_p1_hitbox()

			self.chunks_update(surface) # UPDATE THE VISIBLE CHUNKS

			self.mouse_controller(surface) # UPDATE THE MOUSE POSITION AND WHETHER THE CURSOR IS OVER A BLOCK

			self.Entities(events, surface) # UPDATE THE ENTITIES POSITION

			self.inGameEvents(events) # KEY EVENTS

			self.debugging_Screen(surface, selected_block=self.selected_block)

			self.p1.updateInventory(surface=surface, events=events, mouse=b.mouse_hitbox, keys=self.keys)

			vel = 10

			if self.keys[K_RIGHT]:
				self.CameraMain.add_to_x_coord(value= (-vel * b.deltaTime))

			if self.keys[K_LEFT]:
				self.CameraMain.add_to_x_coord(value= (vel * b.deltaTime))

			if self.keys[K_UP]:
				self.CameraMain.add_to_y_coord(value= (vel * b.deltaTime))

			if self.keys[K_DOWN]:
				self.CameraMain.add_to_y_coord(value= (-vel * b.deltaTime))

			self.pause_screen(surface)

			self.CameraMain.UpdateValues() # UPDATE THE XY VALUES


		elif not self.full_initialation:
			self.init_entities()

			self.init_screen()

	def Entities(self, events, surface):
		self.update_keys_and_mouse()


		classes = self.Entities_man.getEntitiesClasses()
		self.wat = None
		for i in range(len(classes)):
			classes[i].update(surface=surface, chunks_list=self.ActiveChunks, deltaTime=b.deltaTime, camera=self.CameraMain, test=False)
			self.wat = classes[i]

		self.wat.keyMovement(b.deltaTime) # Be able to move the player

		self.update_p1_hitbox()
		self.focus_camera()

	def chunks_update(self, surface):
		self.ActiveChunks = []
		for ch in range(len(self.chunks_list)):
			self.inChunkID = self.chunks_list[ch]["CHUNK_DATA"].is_rect_in_chunk_x_coords(surface=surface, camera=self.CameraMain, Rect=pygame.Rect(self.Entity_hitbox))
			self.ChunkRect = self.chunks_list[ch]["CHUNK_DATA"].get_chunkBlockRect()
			LoadChunk = False

			if self.inChunkID:
				LoadChunk = True

				if self.inChunkID == "None":
					self.inChunkID = self.chunks_list[ch]["CHUNK_DATA"].get_chunk_id()
					self.lastChunkID = self.inChunkID
				else:
					self.lastChunkID = self.inChunkID
					self.inChunkID = self.chunks_list[ch]["CHUNK_DATA"].get_chunk_id()
					self.LastLoadedChunkId = self.inChunkID

				break

		if not self.LastLoadedChunkId == 0:
			self.ActiveChunks.append(self.chunks_list[self.LastLoadedChunkId-1])

		self.ActiveChunks.append(self.chunks_list[self.LastLoadedChunkId])

		if not self.LastLoadedChunkId == len(self.chunks_list)-1:
			self.ActiveChunks.append(self.chunks_list[self.LastLoadedChunkId+1])

		# UPDATE ACTIVECHUNKS
		for c in range(len(self.ActiveChunks)):
			for i in range(len(self.ActiveChunks[c]["BLOCKS"])):
				self.ActiveChunks[c]["BLOCKS"][i].update(deltaTime=b.deltaTime, surface=surface, Camera=self.CameraMain)

	def inGameEvents(self, events):
		
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == K_F3:
					if not self.Pause:
						if self.show_debug_screen:
							self.show_debug_screen = False
						else:
							self.show_debug_screen = True

				elif event.key == K_ESCAPE:
					if not gui.inGui:
						if self.Pause:
							self.Pause = False
						else:
							self.Pause = True

				elif event.key == K_F7:
					self.p1 = random.choice(self.Entities_man.getEntitiesClasses())

			elif event.type == pygame.WINDOWMOVED:
				self.Pause = True

			elif event.type == pygame.WINDOWMINIMIZED:
				self.Pause = True

	def mouse_controller(self, surface):
		self.update_keys_and_mouse() # Update self.mouse and self.keys

		self.camera_size = self.CameraMain.get_camera_size()

		self.selected_block, self.mouse_touching_entity = player_mouse_cotroller(chunks_list=self.ActiveChunks, mouse_hitbox=b.mouse_hitbox, entity_classes=self.classes)

		if not (self.Pause or gui.inGui):
			# Cursor
			pygame.draw.line(surface, (255,255,255), (b.mouse_hitbox[0], 0), (b.mouse_hitbox[0], self.camera_size[1]))
			pygame.draw.line(surface, (255,255,255), (0, b.mouse_hitbox[1]), (self.camera_size[0], b.mouse_hitbox[1]))

			try:
				# Get block id
				block_to_put_id = self.p1.getEntityHotbar().get_slot_item()["Item"][0]
			except:
				block_to_put_id = None

			if self.selected_block != None:
				# Clicks
				block_id = self.selected_block.getId()
				block_position = self.selected_block.getGridCoords()

				if self.mouse[0]:
					placeble_blocks_list[block_id]["class"].break_block(surface=surface, grid_pos=block_position, chunks_list=self.ActiveChunks, deltaTime=b.deltaTime)

				if self.mouse[2]:
					if not block_to_put_id == None:
						if self.selected_block.getId() == 0:
							if self.keys[K_LALT] == 1:
								pass
							else:
								if not self.mouse_touching_entity:
									placeble_blocks_list[block_to_put_id]["class"].place_block(grid_pos=block_position, chunks_list=self.ActiveChunks)

				# See if the selected_block is selected
				if not self.selected_block.isGlowing():
					self.selected_block = None


	def debugging_Screen(self, surface, selected_block):
		""" It shows some variables that may be useful to test """

		player_block_pos = self.p1.get_block_pos()

		if self.show_debug_screen:

			# Chunks blorders
			for c in range(len(self.ActiveChunks)):
				self.ActiveChunks[c]["CHUNK_DATA"].DrawChunkLimits(surface=surface, camera=self.CameraMain)


			self.debug_screen.addDebugText(text=f"FPS: {round(b.fps.get_fps())}", color=(200,0,0))
			
			if not self.foc:
				self.debug_screen.addDebugText(text=f"[Free cam]", color=(170,0,0))

			self.debug_screen.addDebugText(text=f"Terrain seed: {seed}", color=(255,255,255))

			self.debug_screen.addDebugText(text=f"PLAYER POS: {round(player_block_pos[0], 3)}, {round(player_block_pos[1], 3)}", color=(0,200,0))

			self.debug_screen.addDebugText(text=f"CHUNK ID: {self.inChunkID}", color=(255,0,100))

			if self.selected_block != None: 

				self.debug_screen.addDebugText(text=f"Noise Value: {selected_block.getNoiseValue()}", color=(255,255,255))

				self.debug_screen.addDebugText(text=f"Block Pos: {self.selected_block.getGridCoords()}", color=(200,0,0))

				#debug_screen.addDebugText(text=f"isBackground: {selected_block.isBackground()}", color=(255,255,255))

				#debug_screen.addDebugText(text=f"{selected_block.getBreakPorcentage()} %", color=(255,255,255))

			#debug_screen.addDebugText(text=f"CAMERA MAIN COORDS: {a}", color=(0,200,0))
			

			self.debug_screen.Show(surface)

			self.debug_screen.resetDebugList()

	def pause_screen(self, surface):
		if self.Pause:
			pygame.mouse.set_visible(True)
			PauseMenu(surface)
			self.Entities_man.Enable_Physics = False
			self.save_world()

	def update_keys_and_mouse(self):
		self.keys = pygame.key.get_pressed()
		self.mouse = pygame.mouse.get_pressed()

	def focus_camera(self):
		""" Momentarily """
		if self.foc == True:
			# FOCUS CAMERA
			pe_alt = self.p1.get_camera_pos()

			self.CameraMain.set_x_coord(value=(-pe_alt[0] + self.CameraMain.get_camera_size()[0]/2))
			self.CameraMain.set_y_coord(value=(-pe_alt[1] + self.CameraMain.get_camera_size()[1]/2 - 100))

	def update_p1_hitbox(self):
		self.Entity_hitbox = self.p1.get_hitbox()

	def save_world(self):
		save(chunks_list=self.chunks_list)

def game(events, surface):
	global selected_block, block_to_put_id, ActiveChunks, inChunkID, lastChunkID, p1, foc, First, Second, LastLoadedChunkId, init, p1

	First = CameraMain.get_xy()
	
	Second = CameraMain.get_xy()

	global p1_pos, p1_sc_pos
	p1_pos = p1.get_camera_pos()
	p1_sc_pos = p1.get_screen_pos()
	### MOUSE CONTROLLER ###
	

	Debugging_Screen(surface=surface, selected_block=selected_block)
	
	

	# TEST ONLY

	if keys[K_f]:
		if foc:
			foc = False
		else:
			foc = True
		

