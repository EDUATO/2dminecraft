import pygame
import threading
import uuid
import random

from files.import_imp import *
from files.fonts import *
from files.vars import gravity
from files.blocks.Block import *
import files.bucle as b
import files.Game as mg
from files.functions import convert_blocks_pos_to_camera_xy, convert_camera_xy_to_block_pos
from files.gui.hotbar import Hotbar
from files.gui.Inventory import Inventory
from files.gui.Text import Text

class Entity:
	def __init__(self, pos, texture, hitbox_size, camera, body_parts, custom_uuid=False, entity_scale_buff=2):
		self.block_pos = pos # The position is in blocks
		self.pos = list(convert_blocks_pos_to_camera_xy(grid_pos=(-self.block_pos[0], -self.block_pos[1])))

		if custom_uuid:
			self.entity_uuid = custom_uuid
		else:
			self.entity_uuid = uuid.uuid4()

		self.hitbox_size = hitbox_size

		self.camera_updater(Camera=camera)

		self.update_screen_pos()

		self.texture = texture

		self.entity_scale_buff = entity_scale_buff

		self.player_texture = pygame.transform.scale(self.texture, (self.texture.get_width() * self.entity_scale_buff,  self.texture.get_height() * self.entity_scale_buff)) # To the spritesheet

		self.body_parts = body_parts

		self.resized_body_parts = {}

		self.camera_limit_x = self.camera_size
		self.camera_limit_y = 300

		self.physics_variables()

		self.update_hitbox()

		self.Automate_Init() # FOR TESTING PURPOSES

		self.set_Inventory()

		# body 
		self.body_init()

	def body_init(self):
		self.body_parts_keys = list(self.body_parts.keys())
		for i in range(len(self.body_parts)):
			self.resized_body_parts[self.body_parts_keys[i]] = [] # Add a list, so you can append info
			for t in range(4):
				self.resized_body_parts[self.body_parts_keys[i]].append(self.body_parts[self.body_parts_keys[i]][t] * self.entity_scale_buff )

	def body_shape(self,surface, pos, state=0):
		pass

	def DrawTag(self, surface):
		EntityTag = Text(txt=str(self.entity_uuid), x=self.screen_pos[0], y=self.screen_pos[1]-20, FUENTE=Mc_12, COLOR=(255,0,0),lock="x",
					 	screen_areas=(self.screen_pos[0], self.screen_pos[1]-20, self.hitbox_size[0], self.screen_pos[1]-20))

		EntityTag.draw(surface=surface)

	def physics_variables(self):
		self.EnablePhysics = True

		self.vel = 10

		self.vel_y = 0

		self.dy = 0
		self.dx = 0

		self.jumping = False
		self.jump_vel = 16

	def set_Inventory(self):
		self.EntityInventory = Inventory()
		self.EntityHotbar = Hotbar()

	def update_hitbox(self):
		self.hitbox = (self.screen_pos[0], self.screen_pos[1], self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)

	def update(self, surface, chunks_list, deltaTime, camera, test=False):

		self.camera_updater(Camera=camera)
		self.update_screen_pos()
		

		if self.__isEntityOnScreen__():
			self.Enable_Physics()
		else:
			self.Disable_Phyisics()

		self.update_hitbox()

		if mg.Pause == False:
			if self.EnablePhysics:
				collided_blocks = self.nearbyblocks(chunks_list)
				self.physics(collided_blocks, surface, deltaTime=deltaTime)
				self.update_pos()
				self.update_hitbox()

		self.Draw(surface)

		self.dx = 0
		self.dy = 0

		if test:
			self.Automate(deltaTime)

	def updateInventory(self, surface, events, mouse, keys):
		self.EntityInventory.update(surface, mouse, keys)
		self.EntityHotbar.update(events, surface, Inventory_slots=self.EntityInventory.getInventorySlots())
	
	def getEntityHotbar(self):
		return self.EntityHotbar

	def Draw(self, surface):
		self.body_shape(surface, tuple((self.hitbox[0], self.hitbox[1])), 0)
		self.DrawTag(surface)
		#pygame.draw.rect(surface, (255,0,0), pygame.Rect( ( self.screen_pos[0], self.screen_pos[1], self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff) ))


	def nearbyblocks(self, chunks_list):

		# Between all the blocks from the screen detect the ones that are closer to the player
		increaseSize = 100
		biggerHitbox = [ # Make the entity hitbox bigger to detect the surrounding blocks
					(self.hitbox[0]) - increaseSize//2,
					self.hitbox[1] - increaseSize//2,
					self.hitbox[2] + increaseSize,
					self.hitbox[3] + increaseSize
		]
		# dx and dy comprobations
		if self.dx >= 0:
			biggerHitbox[2] += self.dx
		elif self.dx < 0: # Remember self.dx is NEGATIVE
			biggerHitbox[0] += self.dx
			biggerHitbox[2] -= self.dx

		if self.dy >= 0:
			biggerHitbox[3] += self.dy
		elif self.dy < 0: # Remember self.dy is NEGATIVE
			biggerHitbox[1] += self.dy
			biggerHitbox[3] -= self.dy
 
		
		output = []
		for c in range(len(chunks_list)): # Active chunks
			for i in range(len(chunks_list[c]["BLOCKS"])): # Blocks from each chunk
				if chunks_list[c]["BLOCKS"][i].coll_hitbox2(pygame.Rect(biggerHitbox)):
					output.append(chunks_list[c]["BLOCKS"][i])
					#chunks_list[c]["BLOCKS"][i].setglow(True)
		
		return output
			
	def collided_block_tiles(self, blocks_list, rect_formula, ignore=[]):
		blocks_pos = []

		collided_blocks = []
		for i in range(len(blocks_list)):
			blocks_pos.append(blocks_list[i].getGridCoords())
			#blocks_list[i].setglow(True)
			if blocks_list[i].coll_hitbox(Rect=pygame.Rect(rect_formula), undetectable_ids=[0]):
				collided_blocks.append(blocks_list[i])
					

		return collided_blocks

	def get_nearest_block(
		self,
		direction, # left - right - up - bottom
		collided_blocks
		):
		nearest_block = None
		index = 0
		for j in range(len(collided_blocks)):
			self.block = collided_blocks[j] # Blocks that the entity collided

			if direction == "left" or direction == "right":
				index = 0
			elif direction == "up" or direction == "bottom":
				index = 1
			
			grid_pos = self.block.getGridCoords()[index]

			if nearest_block != None:
				if direction == "left" or direction == "up":
					if grid_pos <= nearest_block.getGridCoords()[index]:
						nearest_block = self.block
				elif direction == "right" or direction == "bottom":
					if grid_pos >= nearest_block.getGridCoords()[index]:
						nearest_block = self.block

				nearest_block.setglow(True, color=(200,0,0))
			else: # nearest_block IS None
				nearest_block = self.block

		return nearest_block

	def x_physics(self, every_block_list, surface):
		# Check X collition
		if self.dx >= 0:
			self.x_rect_formula = (self.screen_pos[0], self.screen_pos[1] , (self.hitbox_size[0] * self.entity_scale_buff + self.dx), self.hitbox_size[1] * self.entity_scale_buff)
		elif self.dx < 0: # Will add the NEGATIVE self.dx to screen_pos
			self.x_rect_formula = (self.screen_pos[0] + self.dx, self.screen_pos[1] , (self.hitbox_size[0] * self.entity_scale_buff) - self.dx, self.hitbox_size[1] * self.entity_scale_buff)

		self.x_collided = self.collided_block_tiles(blocks_list=every_block_list, 
													rect_formula=self.x_rect_formula)

		pygame.draw.rect(surface, (255,0,0), pygame.Rect( self.x_rect_formula ))

		if self.dx > 0:
			# Get the leftmost block
			leftmost_block = self.get_nearest_block(direction="left",collided_blocks=self.x_collided)

			if leftmost_block != None:
				self.dx = (leftmost_block.getHitbox().left) - pygame.Rect(self.screen_entity_hitbox).right
				self.entity_collition_type["right"] = True # It colliderected with the right part of the hitbox's entity

		elif self.dx < 0:
			# Get therightmost block
			rightmost_block = self.get_nearest_block(direction="right",collided_blocks=self.x_collided)

			if rightmost_block != None:
				self.dx = (rightmost_block.getHitbox().right) - pygame.Rect(self.screen_entity_hitbox).left
				self.entity_collition_type["left"] = True # It colliderected with the left part of the hitbox's entity

	def y_physics(self, every_block_list, surface):
		# Check Y collition
		if self.dy >= 0:
			self.y_rect_formula = (self.screen_pos[0], self.screen_pos[1] , self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff + self.dy)
		elif self.dy < 0:
			self.y_rect_formula = (self.screen_pos[0], self.screen_pos[1] + self.dy , self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff - self.dy)

		self.y_collided = self.collided_block_tiles(blocks_list=every_block_list, 
													rect_formula=self.y_rect_formula)
		
		if self.dy > 0:
			# Get the highest block
			highest_block = self.get_nearest_block(direction="up", collided_blocks=self.y_collided)

			if highest_block != None:
				self.dy = self.block.getHitbox().top - pygame.Rect(self.screen_entity_hitbox).bottom
				self.vel_y = 0
				self.entity_collition_type["bottom"] = True

		elif self.dy < 0:
			# Get the lowest block
			lowest_block = self.get_nearest_block(direction="bottom", collided_blocks=self.y_collided)

			if lowest_block != None:
				self.dy = self.block.getHitbox().bottom - pygame.Rect(self.screen_entity_hitbox).top
				self.jumping = False
				self.entity_collition_type["top"] = True # good
			
		pygame.draw.rect(surface, (0,0,255), pygame.Rect( self.y_rect_formula ))

		#print(self.entity_collition_type)

	def physics(self, every_block_list, surface, deltaTime=1):
		# Gravity 
		self.vel_y += (1 * deltaTime)
		if self.vel_y > gravity:
			self.vel_y = gravity

		self.dy += (self.vel_y * deltaTime)
		
		self.screen_entity_hitbox = (self.screen_pos[0], self.screen_pos[1], self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)

		self.entity_collition_type = {"right":False, "left":False, "bottom":False, "top":False} #Player's hitbox collition
		
		# X PHYSICS
		self.x_physics(every_block_list, surface)

		# Y PHYSICS
		self.y_physics(every_block_list, surface)
		

	def update_screen_pos(self):
		self.screen_pos = (self.pos[0] + self.CameraXY[0], self.pos[1] + self.CameraXY[1])

	def camera_updater(self, Camera):
		self.CameraMain = Camera
		self.CameraXY = Camera.get_xy()
		self.camera_size = Camera.get_camera_size()
		
	def Disable_Phyisics(self):
		self.EnablePhysics = False

	def Enable_Physics(self):
		self.EnablePhysics = True

	def update_pos(self):
		# Update pos
		self.pos[0] += self.dx
		self.pos[1] += self.dy

	def get_screen_pos(self):
		return self.screen_pos 

	def get_block_pos(self):
		return convert_camera_xy_to_block_pos(xy_pos=(self.get_camera_pos()))

	def get_camera_pos(self):
		return self.CameraMain.convert_screen_pos_to_camera_xy((self.hitbox[0], self.hitbox[1]))

	def get_hitbox(self):
		""" Get the hitbox as a tuple """
		return self.hitbox

	def get_uuid(self):
		return self.entity_uuid

	def move(self, deltaTime, direction=None):
		self.jumping = False
		if direction == "R":
			self.dx += (self.vel * deltaTime)
			
		if direction == "L":
			self.dx -= (self.vel * deltaTime)

		if direction == "U" and self.jumping == False:
			self.vel_y = -self.jump_vel
			self.jumping = True

	def Automate_Init(self):
		self.move_time = 0
		self.Adir = "R"
	def Automate(self, deltaTime):
		self.move(self.Adir, deltaTime)
		self.move_time += 1
		if self.move_time > 300:
			if self.Adir == "R":
				self.Adir = "L"
			else:
				self.Adir = "R"
			
			self.move_time = 0

	def __isEntityOnScreen__(self):
		return isSpriteOnTheScreen(cameraSize=self.camera_size, screenHitbox=pygame.Rect((self.screen_pos[0], self.screen_pos[1], self.hitbox[2], self.hitbox[3])))

		
		

		

		
