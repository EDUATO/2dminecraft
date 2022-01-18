import pygame

from files.vars import win, block_scale_buff, camera_coords

Blocks_list = {
	0 : { "Name" : "Air", "crop" : None },
	1 : { "Name" : "Grass_Block", "crop" : (0,0,16,16) },
	2 : { "Name" : "Stone_Block", "crop" : (16,0,16,16) },
	3 : { "Name" : "Dirt", "crop" : (32,0,16,16)},
	4 : { "Name" : "Oak_Wood", "crop" : (48,0,16,16)},
	5 : { "Name" : "Bedrock", "crop" : (64,0,16,16)}
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

		self.pos_cam = (self.pos[0] + camera_coords[0], self.pos[1] + camera_coords[1])

	def setglow(self, state):
		self.glow = state

	def coordsInBlock(self, coords):
		try:
			if (coords[0] > self.pos_cam[0] and coords[0] < self.pos_cam[0] + (self.block_size[0] * block_scale_buff)) and (coords[1] > self.pos_cam[1] and coords[1] < self.pos_cam[1] + (self.block_size[1] * block_scale_buff)):
				return True
		except IndexError as e:
			print(e)

		return False

	def isGlowing(self):
		return self.glow

	def getGridCoords(self):
		return self.block_pos_grid

	def update(self):
		self.pos_cam = (self.pos[0] + camera_coords[0], self.pos[1] + camera_coords[1])
		if not self.block_id == 0: # isAir
			
			win.blit(self.block_texture, self.pos_cam, tuple(self.crop))

		if self.glow:
			self.select_rect.fill((255,255,0,128))
			win.blit(self.select_rect, tuple(self.pos_cam))

	def coll_hitbox(self, shape):
		if self.block_id != 0: # If is not air
			self.rect_shape = pygame.Rect(shape[0], shape[1], shape[2], shape[3])
			if (self.rect_shape.colliderect(pygame.Rect(self.pos_cam[0], self.pos_cam[1], self.select_rect.get_width(), self.select_rect.get_height()))):
				return True

		return False

	def setBlock(self, id):
		if self.block_id != id:
			self.block_id = id

			self.update_block()

	def getId(self):
		return self.block_id