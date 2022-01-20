import pygame
import threading

from files.import_imp import *
from files.vars import block_scale_buff, gravity, modeX, modeY
from files.Block import *
import files.bucle as b
import files.Game as mg

ENABLE_PHYSICS = True

class Entity:
	def __init__(self, pos, texture, hitbox_size, camera, body_parts,Camera_Focus=False, entity_scale_buff=2):
		self.pos = pos
		self.hitbox_size = hitbox_size

		self.camera_updater(Camera=camera)

		self.texture = texture

		self.entity_scale_buff = entity_scale_buff

		self.player_texture = pygame.transform.scale(self.texture, (self.texture.get_width() * self.entity_scale_buff,  self.texture.get_height() * self.entity_scale_buff)) # To the spritesheet

		self.body_parts = body_parts

		self.resized_body_parts = {}

		self.Camera_Focus = Camera_Focus # If the entity is the main camera
		self.camera_limit_x = modeX
		self.camera_limit_y = 300

		self.vel = 4

		self.vel_y = 0

		self.dy = 0
		self.dx = 0

		self.jumping = False

		self.gamemode = 0

		self.deltaTime = 1


		self.body_parts_keys = list(self.body_parts.keys())
		for i in range(len(self.body_parts)):
			self.resized_body_parts[self.body_parts_keys[i]] = [] # Add a list, so you can append info
			for t in range(4):
				self.resized_body_parts[self.body_parts_keys[i]].append(self.body_parts[self.body_parts_keys[i]][t] * self.entity_scale_buff )


	def body_shape(self,surface, pos, state=0):
		pass

	def update(self, surface, chunks_list, deltaTime, camera):

		self.camera_updater(Camera=camera)

		self.hitbox = (self.pos[0], self.pos[1], self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)

		if mg.Pause == False:
			if ENABLE_PHYSICS:
				collided_blocks = self.nearbyblocks(chunks_list)
				self.physics(collided_blocks) # The phyisics are kind of laggy
				self.update_pos()
		
		self.body_shape(surface, tuple(self.pos), 0)

		self.deltaTime = deltaTime

		self.dx = 0
		self.dy = 0

	def nearbyblocks(self, chunks_list):
		# Between all the blocks from the screen detect the ones that are closer to the player
		increaseSize = 50
		biggerHitbox = ( # Make the entity hitbox bigger to detect the surrounding blocks
					self.hitbox[0] - increaseSize//2,
					self.hitbox[1] - increaseSize,
					self.hitbox[2] + increaseSize,
					self.hitbox[3] + increaseSize*2
		)

		output = []
		for c in range(len(chunks_list)): # Active chunks
			for i in range(len(chunks_list[c])): # Blocks from each chunk
				if chunks_list[c][i]["BLOCK"].coordsInBlock(pygame.Rect(biggerHitbox)):
					output.append(chunks_list[c][i])
					chunks_list[c][i]["BLOCK"].setglow(True)
		
		return output
			

	def physics(self, blocks_list):
		self.oneList = blocks_list
				
					
		# Gravity 
		self.vel_y += (1 * self.deltaTime)
		if self.vel_y > gravity:
			self.vel_y = gravity

		self.dy += (self.vel_y * (self.deltaTime))

		c = 0
		
		# Check collition
		for c in range(len(self.oneList)):
			
			if self.oneList[c]["BLOCK"].getBlockOnScreen():
				
				# X collition
				if self.oneList[c]["BLOCK"].coll_hitbox( (self.pos[0]+ self.dx, self.pos[1] , self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff) ):
					self.dx = 0
					print("UP")
				# Y collition
				if self.oneList[c]["BLOCK"].coll_hitbox( (self.pos[0], self.pos[1] + self.dy, self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff) ):
					# Check if its under the ground
					if self.vel_y < 0:
						self.dy = self.oneList[c]["BLOCK"].getHitbox().bottom - pygame.Rect((self.pos[0], self.pos[1], self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)).top
						self.oneList[c]["BLOCK"].setglow(True)
						self.vel_y = 0

					elif self.vel_y >= 0:
						
						self.hitbox_rect_bottom = pygame.Rect((self.pos[0], self.pos[1], self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)).bottom

						self.dy = self.oneList[c]["BLOCK"].getHitbox().top - self.hitbox_rect_bottom

						self.jumping = False

						self.oneList[c]["BLOCK"].setglow(True)

						self.block_c = self.oneList[c]["BLOCK"].check_block_around_coords(4,4)

						for i in range(len(self.oneList)):
							if self.oneList[i]["POS"] == self.block_c:
								self.oneList[i]["BLOCK"].setglow(True, color=(255,0,255))
								break	
			

	def camera_updater(self, Camera):
		self.CameraMain = Camera
		self.CameraXY = Camera.get_xy()
		

	def update_pos(self):
		# Update pos
		if self.Camera_Focus:
			self.CameraMain.set_x_coord(value=-self.dx, addToTheVar=True)
		else:
			self.pos[0] += self.dx
		
		if self.Camera_Focus:
			self.CameraMain.set_y_coord(value=-self.dy, addToTheVar=True)
		else:
			self.pos[1] += self.dy	

	def get_pos(self):
		return self.pos

	def get_hitbox(self):
		return self.hitbox

	def move(self, direction=None):
		self.jumping = False
		if direction == "R":
			self.dx += (self.vel * self.deltaTime)
			
		if direction == "L":
			self.dx -= (self.vel * self.deltaTime)

		if direction == "W":
			self.dy -= (self.vel * self.deltaTime)

		if direction == "S":
			self.dy += (self.vel * self.deltaTime)

		if direction == "U" and self.jumping == False:
			self.vel_y = -12
			self.jumping = True

	def Automate(self):
		self.move("R")

		
		

		

		
