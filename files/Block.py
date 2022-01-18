import pygame

from files.vars import win, block_scale_buff

Blocks_list = {
	0 : { "Name" : "Air", "crop" : None },
	1 : { "Name" : "Grass_Block", "crop" : (0,0,16,16) },
	2 : { "Name" : "Stone_Block", "crop" : (16,0,16,16) },
	3 : { "Name" : "Dirt", "crop" : (32,0,16,16)}
	}

class Block:
	def __init__(self, texture, ID, block_pos_grid):
		self.block_id = ID
		self.texture = texture
		self.block_texture = pygame.transform.scale(self.texture, (self.texture.get_width() * block_scale_buff,  self.texture.get_height() * block_scale_buff)) # To the spritesheet
		self.pos = []
		self.block_size = [16, 16]
		self.glow = False
		self.block_pos_grid = block_pos_grid

		self.select_rect = pygame.Surface((self.block_size[0] * block_scale_buff, (self.block_size[1] * block_scale_buff)), pygame.SRCALPHA)

		self.update_block(True)

	def update_block(self, init=False):
		if not self.block_id == 0: # isAir
			self.crop = list(Blocks_list[self.block_id]["crop"])
			# Update place to crop
			for i in range(4):
				self.crop[i] = self.crop[i] * block_scale_buff

		if init:
			self.grid(self.block_pos_grid)

	def grid(self, block_pos_grid):
		# x / y
		for i in range(2):
			self.pos.append(block_pos_grid[i] * (self.block_size[i] * block_scale_buff) )

	def setglow(self, state):
		self.glow = state

	def coordsInBlock(self, coords):
		try:
			if (coords[0] > self.pos[0] and coords[0] < self.pos[0] + (self.block_size[0] * block_scale_buff)) and (coords[1] > self.pos[1] and coords[1] < self.pos[1] + (self.block_size[1] * block_scale_buff)):
				return True
		except IndexError as e:
			print(e)

		return False

	def isGlowing(self):
		return self.glow

	def getGridCoords(self):
		return self.block_pos_grid

	def update(self):
		if not self.block_id == 0: # isAir
			
			win.blit(self.block_texture, self.pos, tuple(self.crop))

		if self.glow:
			self.select_rect.fill((255,255,0,128))
			win.blit(self.select_rect, tuple(self.pos))
	def setBlock(self, id):
		if self.block_id != id:
			self.block_id = id

			self.update_block()