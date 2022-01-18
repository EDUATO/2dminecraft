import pygame

from files.import_imp import *
from files.vars import win, block_scale_buff, gravity, modeX, modeY
from files.Block import *


class Entity:
	def __init__(self, pos, texture, hitbox_size, body_parts,camera=False, entity_scale_buff=2):
		self.pos = pos
		self.hitbox_size = hitbox_size

		self.texture = texture

		self.entity_scale_buff = entity_scale_buff

		self.player_texture = pygame.transform.scale(self.texture, (self.texture.get_width() * self.entity_scale_buff,  self.texture.get_height() * self.entity_scale_buff)) # To the spritesheet

		self.body_parts = body_parts

		self.resized_body_parts = {}

		self.camera = camera
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


	def body_shape(self, pos, state=0):
		pass

	def update(self, chunks_list, deltaTime):

		self.physics(chunks_list)
		
		self.body_shape(tuple(self.pos), 0)

		self.hitbox = (self.pos[0], self.pos[1], self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)

		self.deltaTime = deltaTime

		#pygame.draw.rect(win, (255,255,0), self.hitbox, 2)

		

	def physics(self, chunks_list):

		self.oneList = []
		for c in range(len(chunks_list)):
			for i in range(len(chunks_list[c])):
				self.oneList.append(chunks_list[c][i])
				
					
		# Gravity 
		self.vel_y += (1 * self.deltaTime)
		if self.vel_y > gravity:
			self.vel_y = gravity

		self.dy += (self.vel_y * (self.deltaTime))

		c = 0
		# Check collition
		for c in range(len(self.oneList)):
			# X collition
			if self.oneList[c]["BLOCK"].coll_hitbox( (self.pos[0]+ self.dx, self.pos[1] , self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff) ):
				self.dx = 0

			# Y collition
			if self.oneList[c]["BLOCK"].coll_hitbox( (self.pos[0], self.pos[1] + self.dy, self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff) ):
				# Check if its under the ground
				if self.vel_y < 0:
					self.dy = self.oneList[c]["BLOCK"].getHitbox().bottom - pygame.Rect((self.pos[0], self.pos[1], self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)).top
					self.vel_y = 0
				elif self.vel_y >= 0:
					self.dy = self.oneList[c]["BLOCK"].getHitbox().top - pygame.Rect((self.pos[0], self.pos[1], self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)).bottom
					self.jumping = False

				
				
		# Update pos
		if self.camera:
			camera_coords[0] -= self.dx
		else:
			self.pos[0] += self.dx
		
		if self.camera:
			camera_coords[1] -= self.dy
		else:
			self.pos[1] += self.dy	

	def get_pos(self):
		return self.pos

	def get_hitbox(self):
		return self.hitbox

	def move(self, direction=None):

		if direction == "R":
			self.dx += (self.vel * self.deltaTime)
			
		if direction == "L":
			self.dx -= (self.vel * self.deltaTime)

		if direction == "U" and self.jumping == False:
			self.vel_y = -12
			self.jumping = True

		
		

		

		
