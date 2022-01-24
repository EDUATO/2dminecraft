import pygame
import threading

from files.import_imp import *
from files.vars import gravity
from files.Block import *
import files.bucle as b
import files.Game as mg
from files.functions import convert_blocks_pos_to_camera_xy, convert_camera_xy_to_block_pos

ENABLE_PHYSICS = True

class Entity:
	def __init__(self, pos, texture, hitbox_size, camera, body_parts, entity_scale_buff=2):
		self.block_pos = pos # The position is in blocks
		self.pos = list(convert_blocks_pos_to_camera_xy(grid_pos=(-self.block_pos[0], -self.block_pos[1])))

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

		self.vel = 4

		self.vel_y = 0

		self.dy = 0
		self.dx = 0

		self.jumping = False

		self.gamemode = 0

		self.deltaTime = 1

		self.update_hitbox()

		self.Automate_Init() # FOR TESTING PURPOSES

		# body 
		self.body_parts_keys = list(self.body_parts.keys())
		for i in range(len(self.body_parts)):
			self.resized_body_parts[self.body_parts_keys[i]] = [] # Add a list, so you can append info
			for t in range(4):
				self.resized_body_parts[self.body_parts_keys[i]].append(self.body_parts[self.body_parts_keys[i]][t] * self.entity_scale_buff )

	def body_shape(self,surface, pos, state=0):
		pass

	def update_hitbox(self):
		self.hitbox = (self.screen_pos[0], self.screen_pos[1], self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)

	def update(self,surface, chunks_list, deltaTime, camera, test=False):

		self.camera_updater(Camera=camera)

		#self.update_hitbox()

		self.update_screen_pos()

		if mg.Pause == False:
			if ENABLE_PHYSICS:
				collided_blocks = self.nearbyblocks(chunks_list)
				self.physics(collided_blocks, surface)
				self.update_pos()

		self.update_hitbox()

		self.deltaTime = deltaTime

		self.Draw(surface)

		self.dx = 0
		self.dy = 0

		if test:
			self.Automate()

	def Draw(self, surface):
		self.body_shape(surface, tuple(self.screen_pos), 0)

	def nearbyblocks(self, chunks_list):
		# This causes certain lag

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
			for i in range(len(chunks_list[c]["BLOCKS"])): # Blocks from each chunk
				if chunks_list[c]["BLOCKS"][i]["BLOCK"].coll_hitbox2(pygame.Rect(biggerHitbox)):
					output.append(chunks_list[c]["BLOCKS"][i])
					#chunks_list[c][i]["BLOCK"].setglow(True)
		
		return output
			

	def physics(self, blocks_list, surface):
		self.oneList = blocks_list
				
		# Gravity 
		self.vel_y += (1 * self.deltaTime)
		if self.vel_y > gravity:
			self.vel_y = gravity

		self.dy += (self.vel_y * (self.deltaTime))
		
		# Check collition
		for c in range(len(self.oneList)):
			self.block = self.oneList[c]["BLOCK"]
			self.block_pos = self.oneList[c]["POS"]
			self.player_hitbox = pygame.Rect(self.hitbox)
			self.block_hitbox = pygame.Rect(self.oneList[c]["BLOCK"].getHitbox())

			if self.block.getBlockOnScreen():
				
				x_formula = (self.screen_pos[0]+ self.dx, self.screen_pos[1] , self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)

				# X collition
				if self.block.coll_hitbox( pygame.Rect(x_formula), undetectable_ids=[0] ):

					self.dx = 0

				y_formula = (self.screen_pos[0], self.screen_pos[1] + self.dy, self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)
				# Y collition
				if self.block.coll_hitbox( pygame.Rect(y_formula), undetectable_ids=[0] ):
					# Check if its under the ground
					if self.vel_y < 0:
						self.dy = self.block.getHitbox().bottom - pygame.Rect((self.screen_pos[0], self.screen_pos[1], self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)).top
						self.vel_y = 0

					elif self.vel_y >= 0:
						
						self.hitbox_rect_bottom = pygame.Rect((self.screen_pos[0], self.screen_pos[1], self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)).bottom

						self.dy = self.block.getHitbox().top - self.hitbox_rect_bottom

						self.jumping = False

						self.block_c = self.block.check_block_around_coords(4,4)

						for i in range(len(self.oneList)):
							if self.block_pos == self.block_c:
								self.block.setglow(True, color=(255,0,255))
								break	
				
				pygame.draw.rect(surface, (0,0,255), pygame.Rect(x_formula))
				pygame.draw.rect(surface, (255,0,0), pygame.Rect(y_formula))
			

		self.hitbox = (self.player_hitbox.left, self.player_hitbox.right, self.player_hitbox.width, self.player_hitbox.height)

	def update_screen_pos(self):
		self.screen_pos = (self.pos[0] + self.CameraXY[0], self.pos[1] + self.CameraXY[1])

	def camera_updater(self, Camera):
		self.CameraMain = Camera
		self.CameraXY = Camera.get_xy()
		self.camera_size = Camera.get_camera_size()
		

	def update_pos(self):
		# Update pos
		self.pos[0] += self.dx
		self.pos[1] += self.dy

	def get_screen_pos(self):
		return self.screen_pos 

	def get_block_pos(self):
		return convert_camera_xy_to_block_pos(xy_pos=(self.get_camera_pos()))

	def get_camera_pos(self):
		return self.CameraMain.convert_screen_pos_to_camera_xy((self.screen_pos[0], self.screen_pos[1]))

	def get_hitbox(self):
		""" Get the hitbox as a tuple """
		return self.hitbox

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

	def Automate_Init(self):
		self.move_time = 0
		self.Adir = "R"
	def Automate(self):
		self.move(self.Adir)
		self.move_time += 1
		if self.move_time > 300:
			if self.Adir == "R":
				self.Adir = "L"
			else:
				self.Adir = "R"
			
			self.move_time = 0

		
		

		

		
