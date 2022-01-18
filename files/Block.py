import pygame

from files.vars import win, block_scale_buff, camera_coords, block_size
from files.import_imp import Blocks_texture

Blocks_list = {
	0 : { "Name" : "Air", "crop" : None, "durability":False, "special":False },
	1 : { "Name" : "Grass_Block", "crop" : (0,0,16,16), "durability":40, "special":False },
	2 : { "Name" : "Stone_Block", "crop" : (16,0,16,16), "durability":140, "special":False },
	3 : { "Name" : "Dirt", "crop" : (32,0,16,16), "durability":35, "special":False},
	4 : { "Name" : "Oak_Wood", "crop" : (48,0,16,16), "durability":70, "special":False},
	5 : { "Name" : "Bedrock", "crop" : (64,0,16,16), "durability":False, "special":False},
	6 : { "Name" : "Iron Ore", "crop" : (80,0,16,16), "durability":150, "special":False},
	7 : { "Name" : "Wooden Planks", "crop" : (96,0,16,16), "durability":70, "special":False}
	}

Textures_for_blocks_list = {
	0 : { "Name" : "Door1", "crop" : (112,0,16,16), "durability":70},
	1 : { "Name" : "Door2", "crop" : (128,0,16,16), "durability":70}
}

Textures_states = {}

for i in range(9):
	Textures_states[i] = {"Name" : "Break_state_"+str(i), "crop":((16*i)* block_scale_buff, 16* block_scale_buff, 16 * block_scale_buff, 16 * block_scale_buff )}

block_texture = pygame.transform.scale(Blocks_texture, (Blocks_texture.get_width() * block_scale_buff,  Blocks_texture.get_height() * block_scale_buff)) # To the spritesheet

class Block:
	def __init__(self, ID, block_pos_grid):
		self.block_id = ID
		self.color = False
		self.block_texture = block_texture
		self.pos = []
		self.glow = False
		self.block_pos_grid = block_pos_grid
		self.noise_value = False
		self.background = False # No hitbox

		self.break_state = 0

		self.break_durability = 0
		self.break_porcentage = 0

		self.select_rect = pygame.Surface((block_size * block_scale_buff, (block_size * block_scale_buff)), pygame.SRCALPHA)
		self.color_block = pygame.Surface((block_size * block_scale_buff, (block_size * block_scale_buff)), pygame.SRCALPHA)
		self.block_light = pygame.Surface((block_size * block_scale_buff, (block_size * block_scale_buff)), pygame.SRCALPHA).convert_alpha()

		self.update_block(True)

		self.hitbox = pygame.Rect(self.pos[0] + camera_coords[0], self.pos[1] + camera_coords[1], self.select_rect.get_width(), self.select_rect.get_height())

		self.deltaTime = 1

		self.Breakeable = True

		self.light_val = 0

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
		# x / y
		for i in range(2):
			self.pos.append(block_pos_grid[i] * (block_size * block_scale_buff) )

		self.pos_cam = (self.pos[0] + camera_coords[0], self.pos[1] + camera_coords[1])

	def setglow(self, state):
		self.glow = state

	def coordsInBlock(self, coords):
		try:
			if (coords[0] >= self.pos_cam[0] and coords[0] < self.pos_cam[0] + (block_size * block_scale_buff)) and (coords[1] >= self.pos_cam[1] and coords[1] < self.pos_cam[1] + (block_size * block_scale_buff)):
				return True
		except IndexError as e:
			print(e)

		return False

	def isGlowing(self):
		return self.glow

	def getGridCoords(self):
		return self.block_pos_grid

	def update(self, deltaTime):
		self.pos_cam = (self.pos[0] + camera_coords[0], self.pos[1] + camera_coords[1])
		if not self.block_id == 0: # isAir
			try:
				# Crop block from texture
				win.blit(self.block_texture, self.pos_cam, tuple(self.crop))
			except:
				pass

		self.deltaTime = deltaTime

		if not self.color == False:
			self.color_block.fill(self.color)
			win.blit(self.color_block, tuple(self.pos_cam))

		# Update durability
		self.break_durability = Blocks_list[self.block_id]["durability"]

		# Update hitbox 
		self.hitbox = pygame.Rect(self.pos_cam[0], self.pos_cam[1], self.select_rect.get_width(), self.select_rect.get_height())

		# Block light
		if not self.block_id == 0:
			self.block_light.fill((0,0,0,self.light_val))
			win.blit(self.block_light, tuple(self.pos_cam))


		if self.glow:
			self.select_rect.fill((255,255,0,128))
			win.blit(self.select_rect, tuple(self.pos_cam))

	def coll_hitbox(self, shape):
		if self.block_id != 0: # If is not air
			self.rect_shape = pygame.Rect(shape[0], shape[1], shape[2], shape[3])
			if (self.rect_shape.colliderect(self.hitbox)
				and self.background == False):
				# Show hitbox
				#pygame.draw.rect(win, (0,255,0), self.hitbox)
				return True

		return False

	def getHitbox(self):
		return self.hitbox

	def setBlock(self, id, color=False, noiseValue=False, background=False):
		self.color = color
		if self.block_id != id and self.Breakeable == True:
			if color == False:
				self.block_id = id

			self.noise_value = noiseValue
				
			self.background = background

			self.update_block()

	def breakBlock(self, id):
		if not self.break_durability == False:
			self.break_state += (1 * self.deltaTime)

			try:
				self.break_porcentage =  100 * self.break_state // self.break_durability
			except ZeroDivisionError:
				pass

			for i in range(9):
				if self.break_porcentage >= ( (i+1) * 10) and self.break_porcentage < ( (i+2) * 10):
					win.blit(self.block_texture, self.pos_cam, Textures_states[i]["crop"])
					break

			if self.break_state >= self.break_durability:
				self.block_id = id
				self.resetBreakState()

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