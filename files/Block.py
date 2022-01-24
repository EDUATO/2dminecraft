import pygame

from files.vars import block_scale_buff, block_size
from files.block_data import *
from files.functions import isSpriteOnTheScreen

Textures_states = {}

for i in range(9):
	Textures_states[i] = {"Name" : "Break_state_"+str(i), "crop":((16*i)* block_scale_buff, 16* block_scale_buff, 16 * block_scale_buff, 16 * block_scale_buff )}

class Block:
	def __init__(self, ID, block_pos_grid, Camera):
		self.block_id = ID
		self.color = False
		self.block_texture = block_texture
		self.pos = []
		self.glow = False
		self.glow_color = (255,255,0)
		self.block_pos_grid = block_pos_grid # Block Position in grid
		self.noise_value = False
		self.background = False # No hitbox

		# Camera
		self.camera_updater(Camera=Camera)

		self.break_state = 0

		self.break_durability = 0
		self.break_porcentage = 0

		self.block_size = (block_size * block_scale_buff), (block_size * block_scale_buff)

		self.select_rect = pygame.Surface((self.block_size), pygame.SRCALPHA).convert_alpha()
		self.color_block = pygame.Surface((self.block_size), pygame.SRCALPHA).convert()
		self.block_light = pygame.Surface((self.block_size), pygame.SRCALPHA).convert_alpha()

		self.update_block(True)

		self.hitbox = pygame.Rect(self.pos[0] + self.CameraXY[0], self.pos[1] + self.CameraXY[1], self.block_size[0], self.block_size[1])

		self.deltaTime = 1

		self.Breakeable = True

		self.light_val = 45
		self.background_val = 30

		self.BlockOnScreen = False

	def camera_updater(self, Camera):
		self.CameraMain = Camera
		self.CameraXY = Camera.get_xy()
		self.camera_size = Camera.get_camera_size()

	def update_block(self, init=False):
		if not self.block_id == 0: # isAir
			if self.color == False:
				self.crop = list(Blocks_list[self.block_id]["crop"])
				# Update place to crop
				for i in range(4):
					self.crop[i] = self.crop[i] * block_scale_buff

		if init:
			self.grid(self.block_pos_grid)

	def grid(self, block_pos_grid):
		# Set the pixel position for each block
		# x / y
		for i in range(2):
			if i == 0:
				self.pos.append(block_pos_grid[i] * (block_size * block_scale_buff)) 
			elif i == 1:
				self.pos.append( -(block_pos_grid[i]) * (block_size * block_scale_buff)) 
			

		self.pos_cam = (self.pos[0] + self.CameraXY[0], self.pos[1] + self.CameraXY[1])

	def setglow(self, state, color=(255,255,0)):
		self.glow = state
		self.glow_color = color

	def update(self, surface, deltaTime, Camera):
		self.camera_updater(Camera)

		self.pos_cam = (self.pos[0] + self.CameraXY[0], self.pos[1] + self.CameraXY[1])

		# Update hitbox 
		self.hitbox = pygame.Rect(self.pos_cam[0], self.pos_cam[1], self.select_rect.get_width(), self.select_rect.get_height())

		self.DrawOnScreen(surface, deltaTime)

	def DrawOnScreen(self, surface, deltaTime):
		self.BlockOnScreen = self.__isBlockOnScreen__()

		if self.BlockOnScreen:

			if not self.block_id == 0: # isAir
				# Crop block from texture
				surface.blit(self.block_texture, self.pos_cam, tuple(self.crop))

			self.deltaTime = deltaTime

			if not self.color == False:
				self.color_block.fill(self.color)
				surface.blit(self.color_block, tuple(self.pos_cam))

			# Update durability
			self.break_durability = Blocks_list[self.block_id]["durability"]

			# LIGHT
			self.block_light.fill((0,0,0, self.light_val))
			if self.background:
				# Block light in background
				if (self.background_val + self.light_val) > 255: self.block_light.fill((0,0,0,255))
				else: self.block_light.fill((0,0,0,self.background_val + self.light_val))
					

			surface.blit(self.block_light, tuple(self.pos_cam))


			if self.glow:
				self.select_rect.fill((self.glow_color[0],self.glow_color[1],self.glow_color[2],128))
				surface.blit(self.select_rect, tuple(self.pos_cam))

	def coll_hitbox(self, Rect, undetectable_ids=[]):
		""" Check if a Rect is colliderecting with the block """
		if (self.block_id not in undetectable_ids):
			if not self.background:
				return self.__hitbox_coll__(Rect)

	def coll_hitbox2(self, Rect):
		""" Check if a Rect is colliderecting with EVERY block (FASTER THAN coll_hitbox)"""
		return self.__hitbox_coll__(Rect)

		
	def check_block_around_coords(self, xval, yval): 
		# Check the coords from a specific block starting from the initial block coords
		return (self.block_pos_grid[0] + xval, self.block_pos_grid[1] + yval )


	def setBlock(self, id, color=False, noiseValue=False, background=False):
		self.color = color
		if self.block_id != id and self.Breakeable == True:
			if color == False:
				self.block_id = id

			self.noise_value = noiseValue
				
			self.background = background

			self.update_block()

	def breakBlock(self, surface, id):
		if not self.break_durability == False:
			self.break_state += (1 * self.deltaTime)

			try:
				self.break_porcentage =  100 * self.break_state // self.break_durability
			except ZeroDivisionError:
				pass

			for i in range(9):
				if self.break_porcentage >= ( (i+1) * 10) and self.break_porcentage < ( (i+2) * 10):
					surface.blit(self.block_texture, self.pos_cam, Textures_states[i]["crop"])
					break

			if self.break_state >= self.break_durability:
				self.block_id = id
				self.resetBreakState()

				self.background = False

	def getBreakPorcentage(self):
		return self.break_porcentage

	def resetBreakState(self):
		self.break_state = 0
		self.break_porcentage = 0

	def getId(self):
		return self.block_id

	def setBreakeable(self, state):
		self.Breakeable = state

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

	def getGridCoords(self):
		return self.block_pos_grid

	def get_pos(self):
		return self.pos

	def getHitbox(self):
		return self.hitbox

	def set_light_val(self, value):
		""" Set shadow block value. (up to 255) """
		self.light_val = value

	def __hitbox_coll__(self, Rect):
		if Rect.colliderect(self.hitbox):
			return True

		return False

	def __isBlockOnScreen__(self):
		if isSpriteOnTheScreen(camera=self.pos_cam, screenSize=self.camera_size, hitboxSize=(block_size * block_scale_buff, block_size * block_scale_buff)):
			return True
		return False