import pygame, random

from files.vars import block_scale_buff, block_size, block_detection_after_screen
from files.blocks.every_block_data import get_every_block_list
from files.functions import isSpriteOnTheScreen, change_sprite_color

Textures_states = {}

for i in range(9):
	Textures_states[i] = {"Name" : "Break_state_"+str(i), "crop":((16*i)* block_scale_buff, 16* block_scale_buff, 16 * block_scale_buff, 16 * block_scale_buff )}

class Block:
	def __init__(self, App, block_pos_grid, colored_sprite_rgb=False):
		self.block_id = 0 # At first it will always be air
		self.block_texture = App.assets.Block_texture_tr
		
		self.pos = []
		self.glow = False
		self.glow_color = (255,255,0)
		self.block_pos_grid = block_pos_grid # Block Position in grid
		self.noise_value = False
		self.background = True # No hitbox
		self.set_colored_sprite(colored_sprite_rgb)
		self.instant_block_break = False

		self.break_durability = 0
		self.break_state = 0

		self.break_porcentage = 0

		self.block_size = (block_size * block_scale_buff), (block_size * block_scale_buff)

		self.select_rect = pygame.Surface((self.block_size), pygame.SRCALPHA).convert_alpha()
		self.color_block = pygame.Surface((self.block_size), pygame.SRCALPHA).convert()
		self.block_light = pygame.Surface((self.block_size), pygame.SRCALPHA).convert_alpha()

		self.color = False

		self.light_val = 0
		self.background_val = 30

		self.BlockOnScreen = False

		### UPDATERS ###

		self.update_block()

		self.grid(self.block_pos_grid)

		self.screen_pos = (self.pos[0], self.pos[1])
		self.update_hitbox()

		self.every_block_list = get_every_block_list(App)

	def set_colored_sprite(self, color):
		self.new_colored_sprite = None
		if color:
			self.new_colored_sprite = change_sprite_color(self.block_texture, color)

	def camera_updater(self, Camera):
		self.CameraMain = Camera
		self.CameraXY = Camera.get_xy()
		self.camera_size = Camera.get_camera_size()

	def update_block(self):
		if not self.block_id == 0: # isAir
			self.crop = list(self.every_block_list[self.block_id]["crop"])
			# Update place to crop
			for i in range(4):
				self.crop[i] = self.crop[i] * block_scale_buff

	def update_screen_pos(self):
		self.screen_pos = (self.pos[0] + self.CameraXY[0], self.pos[1] + self.CameraXY[1])

	def update_hitbox(self):
		self.hitbox = pygame.Rect(self.screen_pos[0], self.screen_pos[1], self.select_rect.get_width(), self.select_rect.get_height())

	def grid(self, block_pos_grid):
		# Set the pixel position for each block
		# x / y
		self.pos.append(block_pos_grid[0] * (block_size * block_scale_buff))

		self.pos.append(-block_pos_grid[1] * (block_size * block_scale_buff))

	def update(self, App, deltaTime, Camera):
		self.camera_updater(Camera)

		self.update_screen_pos()

		self.update_hitbox()

		self.DrawOnScreen(App, deltaTime)

	def DrawOnScreen(self, App, deltaTime):
		self.BlockOnScreen = self.isBlockOnScreen()
		if self.BlockOnScreen:

			if not( self.block_id == 0 or self.color): # isAir
				self.DrawBlock(App)
				if self.color:
					self.color_block.fill(self.color)
					surface.blit(self.color_block, tuple(self.screen_pos))

				# LIGHT
				self.block_light_engine(App)

				if self.glow:
					self.select_rect.fill((self.glow_color[0],self.glow_color[1],self.glow_color[2],128))
					App.surface.blit(self.select_rect, tuple(self.screen_pos))


	def block_light_engine(self, App):
	
		self.block_light.fill((0,0,0, self.light_val))
		if self.background:
			# Block light in background
			if (self.background_val + self.light_val) > 255: self.block_light.fill((0,0,0,255))
			else: self.block_light.fill((0,0,0,self.background_val + self.light_val))
			
		App.surface.blit(self.block_light, tuple(self.screen_pos))

	def DrawBlock(self, App):
		# Crop block from texture and draw it on the screen
		if self.new_colored_sprite:
			# Colored blocks, like leaves
			App.surface.blit(self.new_colored_sprite, self.screen_pos, tuple(self.crop))
		else:
			App.surface.blit(self.block_texture, self.screen_pos, tuple(self.crop))

	def coll_hitbox(self, Rect, undetectable_ids=[]):
		""" Check if a Rect is colliderecting with the block """
		if (self.block_id not in undetectable_ids):
			if not self.background:
				return self.__hitbox_coll__(Rect)

	def coll_hitbox2(self, Rect):
		""" Check if a Rect is colliderecting with EVERY block (FASTER THAN coll_hitbox)"""
		return self.__hitbox_coll__(Rect)

	def setBlock(self, id, noiseValue=False, background=False, color=False):
		""" Place a block"""
		self.block_id = id
		self.color = color

		self.noise_value = noiseValue
			
		self.background = background

		self.update_block()

	def breakBlock(self, App, deltaTime):

		if self.break_durability != False:
			self.break_state += (1 * deltaTime)

			self.break_porcentage =  100 * self.break_state // self.break_durability
			if not self.instant_block_break:
				for i in range(9):
					if self.break_porcentage >= ( (i+1) * 10) and self.break_porcentage < ( (i+2) * 10):
						App.surface.blit(self.block_texture, self.screen_pos, Textures_states[i]["crop"])
						break

				if self.break_state >= self.break_durability:
					self.ForceBreakBlock()
			else:
				self.ForceBreakBlock()

	def ForceBreakBlock(self):
		self.block_id = 0 # Set the block as 'air'
		self.break_durability = 0
		self.resetBreakState()

		self.background = False

	def getBreakPorcentage(self):
		return self.break_porcentage

	def resetBreakState(self):
		self.break_state = 0
		self.break_porcentage = 0

	def getId(self):
		return self.block_id

	def setglow(self, state, color=(255,255,0)):
		self.glow = state
		self.glow_color = color

	def getNoiseValue(self):
		return self.noise_value

	def setBackground(self, state):
		self.background = state

	def isBackground(self):
		return self.background

	def getBlockOnScreen(self):
		return self.BlockOnScreen

	def isGlowing(self):
		return self.glow

	def get_screen_pos(self):
		return self.screen_pos

	def getHitbox(self):
		return self.hitbox

	def getGridCoords(self):
		return self.block_pos_grid

	def set_light_val(self, value):
		""" Set shadow block value. (up to 255) """
		self.light_val = value

	def isBlockOnScreen(self):
		return isSpriteOnTheScreen(cameraSize=self.camera_size, screenHitbox=self.hitbox)

	def blockDetection(self):
		return isSpriteOnTheScreen(
			cameraSize= (self.camera_size[0] + block_detection_after_screen*self.block_size[0], self.camera_size[0] + block_detection_after_screen*self.block_size[1]), 
			screenHitbox= self.hitbox,
			startCameraPos=(-(block_detection_after_screen*self.block_size[0]), -(block_detection_after_screen*self.block_size[1]) ))

	def __hitbox_coll__(self, Rect):
		return Rect.colliderect(self.hitbox)