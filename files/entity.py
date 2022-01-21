import pygame
import threading

from files.import_imp import *
from files.vars import gravity
from files.Block import *
import files.bucle as b
import files.Game as mg
from files.functions import convert_blocks_pos_to_camera_xy

ENABLE_PHYSICS = True

class Entity:
	def __init__(self, pos, texture, hitbox_size, camera, body_parts, entity_scale_buff=2):
		self.block_pos = pos # The position is in blocks
		self.pos = list(convert_blocks_pos_to_camera_xy(grid_pos=(-self.block_pos[0], -self.block_pos[1])))
		print(f"TRUE POS: {self.pos}")

		self.hitbox_size = hitbox_size

		self.camera_updater(Camera=camera)

		self.update_camera_pos()

		self.texture = texture

		self.entity_scale_buff = entity_scale_buff

		self.player_texture = pygame.transform.scale(self.texture, (self.texture.get_width() * self.entity_scale_buff,  self.texture.get_height() * self.entity_scale_buff)) # To the spritesheet

		self.body_parts = body_parts

		self.resized_body_parts = {}

		self.camera_limit_x = self.camera_size
		self.camera_limit_y = 300

		self.vel = 4

		self.vel_y = 0

		self.dy = 0
		self.dx = 0

		self.jumping = False

		self.gamemode = 0

		self.deltaTime = 1

		# body 
		self.body_parts_keys = list(self.body_parts.keys())
		for i in range(len(self.body_parts)):
			self.resized_body_parts[self.body_parts_keys[i]] = [] # Add a list, so you can append info
			for t in range(4):
				self.resized_body_parts[self.body_parts_keys[i]].append(self.body_parts[self.body_parts_keys[i]][t] * self.entity_scale_buff )

	def body_shape(self,surface, pos, state=0):
		pass

	def update(self, surface, chunks_list, deltaTime, camera):

		self.camera_updater(Camera=camera)

		self.hitbox = (self.cam_pos[0], self.cam_pos[1], self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)

		if mg.Pause == False:
			if ENABLE_PHYSICS:
				collided_blocks = self.nearbyblocks(chunks_list)
				self.physics(collided_blocks) # The phyisics are kind of laggy
				self.update_pos()
		
		self.body_shape(surface, tuple(self.cam_pos), 0)

		self.deltaTime = deltaTime

		self.dx = 0
		self.dy = 0

	def nearbyblocks(self, chunks_list):
		# Between all the blocks from the screen detect the ones that are closer to the player
		increaseSize = 50
		biggerHitbox = ( # Make the entity hitbox bigger to detect the surrounding blocks
					self.hitbox[0] - increaseSize//2,
					self.hitbox[1] - increaseSize//2,
					self.hitbox[2] + increaseSize,
					self.hitbox[3] + increaseSize
		)

		output = []
		for c in range(len(chunks_list)): # Active chunks
			for i in range(len(chunks_list[c])): # Blocks from each chunk
				if chunks_list[c][i]["BLOCK"].coll_hitbox2(pygame.Rect(biggerHitbox)):
					output.append(chunks_list[c][i])
					#chunks_list[c][i]["BLOCK"].setglow(True)
		
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
				
				x_formula = (self.cam_pos[0]+ self.dx, self.cam_pos[1] , self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)
				# X collition
				if self.oneList[c]["BLOCK"].coll_hitbox( pygame.Rect(x_formula), undetectable_ids=[0] ):
					self.dx = 0

				y_formula = (self.cam_pos[0], self.cam_pos[1] + self.dy, self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)
				# Y collition
				if self.oneList[c]["BLOCK"].coll_hitbox( pygame.Rect(y_formula), undetectable_ids=[0] ):
					# Check if its under the ground
					if self.vel_y < 0:
						self.dy = self.oneList[c]["BLOCK"].getHitbox().bottom - pygame.Rect((self.cam_pos[0], self.cam_pos[1], self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)).top
						self.vel_y = 0

					elif self.vel_y >= 0:
						
						self.hitbox_rect_bottom = pygame.Rect((self.cam_pos[0], self.cam_pos[1], self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)).bottom

						self.dy = self.oneList[c]["BLOCK"].getHitbox().top - self.hitbox_rect_bottom

						self.jumping = False

						self.block_c = self.oneList[c]["BLOCK"].check_block_around_coords(4,4)

						for i in range(len(self.oneList)):
							if self.oneList[i]["POS"] == self.block_c:
								self.oneList[i]["BLOCK"].setglow(True, color=(255,0,255))
								break	
			
	def update_camera_pos(self):
		self.cam_pos = (self.pos[0] + self.CameraXY[0], self.pos[1] + self.CameraXY[1])

	def camera_updater(self, Camera):
		self.CameraMain = Camera
		self.CameraXY = Camera.get_xy()
		self.camera_size = Camera.get_camera_size()
		

	def update_pos(self):
		# Update pos
		self.pos[0] += self.dx
		self.pos[1] += self.dy

		self.update_camera_pos()

	def get_camera_pos(self):
		return self.cam_pos #FIX

	def get_hitbox(self):
		return self.hitbox

	def move(self, direction=None):
		self.jumping = False
		if direction == "R":
			self.dx += (self.vel * self.deltaTime)
			
		if direction == "L":
			self.dx -= (self.vel * self.deltaTime)

		if direction == "U" and self.jumping == False:
			self.vel_y = -12
			self.jumping = True

	def Automate(self):
		self.move("R")

		
		

		

		
