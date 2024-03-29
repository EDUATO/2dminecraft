import pygame
import random
import time
import threading
import math

########## LOCAL MODULES ##########
from files.vars import Scene, block_scale_buff, DebugScreen, block_size, chunk_size, block_to_put_id, modeY, structure_manager_list
import files.functions as f
from files.grid import grid
import files.gui.gui_class as gui
from files.entity.player_mouse_controller import player_mouse_cotroller
from files.gui.pauseMenu import PauseMenu
from files.saving.gamesave import save
from files.terrain.chunk import Chunk
from files.terrain.terrain_generator import chunk_manager_list

from files.classes_init import * # Game's classes and vars initialization

class Game(Game_Initialization):
	def __init__(self, App):
		super().__init__(App)

		self.init_blocks()

		self.LastLoadedChunkId = 0

		self.lastChunkID = "None"

		self.foc = True

		self.Pause = False

	def update(self, App, running_threads_amount=None):
		
		if self.full_initialation:
			self.classes = self.Entities_man.getEntitiesClasses()
			# Clear screen
			App.surface.fill((154,203,255))

			self.chunks_update(App) # UPDATE THE VISIBLE CHUNKS

			self.update_p1_hitbox()

			self.Entities(App) # UPDATE THE ENTITIES POSITION

			if not self.Pause:
				self.mouse_controller(App) # UPDATE THE MOUSE POSITION AND WHETHER THE CURSOR IS OVER A BLOCK

			self.inGameEvents(App) # KEY EVENTS

			self.debugging_Screen(App, selected_block=self.selected_block, running_threads_amount=running_threads_amount)
				

			if not self.Pause:
				if not gui.inGui[1] == False:
					gui.inGui[1].update(App, keys=self.keys)
				self.p1.updateInventory(App, keys=self.keys)

				vel = 10

				if self.keys[pygame.K_RIGHT]:
					self.CameraMain.add_to_x_coord(value= -(vel * App.deltaTime))

				if self.keys[pygame.K_LEFT]:
					self.CameraMain.add_to_x_coord(value= (vel * App.deltaTime))

				if self.keys[pygame.K_UP]:
					self.CameraMain.add_to_y_coord(value= (vel * App.deltaTime))

				if self.keys[pygame.K_DOWN]:
					self.CameraMain.add_to_y_coord(value= -(vel * App.deltaTime))

			self.pause_screen(App)

			self.CameraMain.UpdateValues() # UPDATE THE XY VALUES


		elif not self.full_initialation:
			self.init_screen()

	def Entities(self, App):
		self.update_keys_and_mouse()

		classes = self.Entities_man.getEntitiesClasses()
		self.wat = None
		for i in range(len(classes)):
			
			if classes[i].get_uuid() != self.p1_uuid:
				classes[i].update(App,App, chunks_list=self.ActiveChunks, deltaTime=App.deltaTime, camera=self.CameraMain)
				#classes[i].Automate(App.deltaTime)
			else:
				self.wat = classes[i]
				self.wat.show_tag = False

		if not self.Pause:
			self.wat.keyMovement(App.deltaTime) # Be able to move the player
		self.wat.update(App=App, chunks_list=self.ActiveChunks, deltaTime=App.deltaTime, camera=self.CameraMain)
		self.wat_hitbox = self.wat.get_hitbox()

		self.update_p1_hitbox()
		self.focus_camera()

	def chunks_update(self, App):
		self.ActiveChunks = []
		
		try:
			self.inChunkID = f.detect_chunk_with_position(self.p1.get_block_pos())
		except: self.inChunkID = 0

		self.Chunks_to_draw = [self.inChunkID-1, self.inChunkID, self.inChunkID+1]

		self.player_in_chunk = None
		for chunk in chunks_list:
			if chunk.Chunk_ID in self.Chunks_to_draw:
				self.ActiveChunks.append(chunk)
				if chunk.Chunk_ID == self.inChunkID:
					self.player_in_chunk = chunk

		# Seek for non generated chunks
		for ch_id in self.Chunks_to_draw:
			if not self.detect_non_generated_chunk(ch_id):
				chunk_manager_list.append(ch_id)
			
		structs_to_draw = []
		for struct in structure_manager_list:
			if struct.center_pos_chunk in self.Chunks_to_draw:
				for i in range(len(struct.blocks_list)): 
					structs_to_draw.append(struct.blocks_list[i])
				
			structure_manager_list.remove(struct)

			

		# UPDATE ACTIVECHUNKS
		for chunk in self.ActiveChunks:
			for i in range(len(chunk.blocks)):
				for block in structs_to_draw:
					if block["pos"] == chunk.blocks[i].block_pos_grid:
						self.placeble_blocks_list[block["id"]]["class"].place_generated_block(App, chunk.blocks[i])
				
				chunk.blocks[i].update(App=App, deltaTime=App.deltaTime, Camera=self.CameraMain)
			

		

	def detect_non_generated_chunk(self, chunk_id):
		isChunk = False
		for chunk in chunks_list:
			if chunk.get_chunk_id() == chunk_id:
				isChunk = True
				break

		return isChunk

	def inGameEvents(self, App):
		
		for event in App.events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_F3:
					if not self.Pause:
						if self.show_debug_screen:
							self.show_debug_screen = False
						else:
							self.show_debug_screen = True

				elif event.key == pygame.K_ESCAPE:
					if not gui.inGui[0]:
						if self.Pause:
							self.Pause = False
						else:
							self.Pause = True

				elif event.key == pygame.K_l:
					self.Entities_man.spawnEntity(self.CameraMain, type="Wty", Blockpos=self.p1.get_block_pos(), bot=True)
				elif event.key == pygame.K_c:
					self.Entities_man.spawnEntity(self.CameraMain, type="Creeper", Blockpos=self.p1.get_block_pos())

				elif event.key == pygame.K_F7:
					self.p1 = random.choice(self.Entities_man.getEntitiesClasses())

			elif event.type == pygame.WINDOWMOVED:
				self.Pause = True

			elif event.type == pygame.WINDOWMINIMIZED:
				self.Pause = True

	def mouse_controller(self, App):
		self.update_keys_and_mouse() # Update self.mouse and self.keys

		self.camera_size = self.CameraMain.get_camera_size()

		self.selected_block, self.mouse_touching_entity = player_mouse_cotroller(chunks_list=self.ActiveChunks, mouse_hitbox=App.mouse_hitbox, entity_classes=self.classes)

		if not (self.Pause or gui.inGui[0]):
			# Cursor
			pygame.draw.line(App.surface, (255,255,255), (App.mouse_hitbox[0], 0), (App.mouse_hitbox[0], self.camera_size[1]))
			pygame.draw.line(App.surface, (255,255,255), (0, App.mouse_hitbox[1]), (self.camera_size[0], App.mouse_hitbox[1]))

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
					self.placeble_blocks_list[block_id]["class"].break_block(App=App, grid_pos=block_position, chunks_list=self.ActiveChunks, deltaTime=App.deltaTime)
				else: self.selected_block.resetBreakState()

				if self.mouse[2]:
					if not block_to_put_id == None:
						if self.selected_block.getId() == 0: # isAir
							if self.keys[K_LALT] == 1:
								pass
							else:
								if not self.mouse_touching_entity:
									self.placeble_blocks_list[block_to_put_id]["class"].place_block(App=App, grid_pos=block_position, chunks_list=self.ActiveChunks)
					if self.placeble_blocks_list[block_id]["class"].block_id != 0:
						self.placeble_blocks_list[block_id]["class"].rightClickAction(block=self.selected_block, game=self)

				# See if the selected_block is selected
				if not self.selected_block.isGlowing():
					self.selected_block = None


	def debugging_Screen(self, App, selected_block, running_threads_amount=None):
		""" It shows some variables that may be useful to test """

		player_block_pos = self.p1.get_block_pos()
		collision_player = self.p1.EntityPhysics.entity_collition_type

		if self.show_debug_screen:

			# Chunks blorders
			for c in range(len(self.ActiveChunks)):
				self.ActiveChunks[c].DrawChunkLimits(App=App, camera=self.CameraMain)


			self.debug_screen.addDebugText(text=f"FPS: {round(App.fps.get_fps())}", color=(200,0,0))
			
			self.debug_screen.addDebugText(text=f"Running threads: {running_threads_amount}", color=(200,0,200))

			if not self.foc:
				self.debug_screen.addDebugText(text=f"[Free cam]", color=(170,0,0))

			self.debug_screen.addDebugText(text=f"Terrain seed: {seed}", color=(255,255,255))

			self.debug_screen.addDebugText(text=f"PLAYER POS: {round(player_block_pos[0], 3)}, {round(player_block_pos[1], 3)}", color=(0,200,0))

			self.debug_screen.addDebugText(text=f"CHUNK ID: {self.inChunkID}", color=(255,0,100))

			try:
				self.debug_screen.addDebugText(text=f"Chunk Generated: {self.player_in_chunk.isGenerated}", color=(255,0,100))
			except AttributeError: pass

			if self.selected_block != None: 

				self.debug_screen.addDebugText(text=f"Noise Value: {selected_block.getNoiseValue()}", color=(255,255,255))

				self.debug_screen.addDebugText(text=f"Block Pos: {self.selected_block.getGridCoords()}", color=(200,0,0))

				#debug_screen.addDebugText(text=f"isBackground: {selected_block.isBackground()}", color=(255,255,255))

				#debug_screen.addDebugText(text=f"{selected_block.getBreakPorcentage()} %", color=(255,255,255))

			self.debug_screen.addDebugText(text=f"Right: {collision_player['right']}", color=(0,170,0))
			self.debug_screen.addDebugText(text=f"Left: {collision_player['left']}", color=(0,170,0))
			self.debug_screen.addDebugText(text=f"Top: {collision_player['top']}", color=(0,170,0))
			self.debug_screen.addDebugText(text=f"Bottom: {collision_player['bottom']}", color=(0,170,0))

			#debug_screen.addDebugText(text=f"CAMERA MAIN COORDS: {a}", color=(0,200,0))
			

			self.debug_screen.Show(App)

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
		"""save(chunks_list=self.chunks_list)"""
		pass
		

