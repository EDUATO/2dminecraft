import pygame
import threading
import uuid

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
		EntityTag = Text(txt=str(self.entity_uuid), x=self.screen_pos[0], y=self.screen_pos[1]-20, FUENTE=Mc_15, COLOR=(255,0,0),
					 	screen_areas=(self.screen_pos[0], self.screen_pos[1]-20, self.hitbox_size[0], self.screen_pos[1]-20))

		EntityTag.draw(surface=surface)

	def physics_variables(self):
		self.EnablePhysics = True

		self.vel = 4

		self.vel_y = 0

		self.dy = 0
		self.dx = 0

		self.jumping = False

	def set_Inventory(self):
		self.EntityInventory = Inventory()
		self.EntityHotbar = Hotbar()

	def update_hitbox(self):
		self.hitbox = (self.screen_pos[0], self.screen_pos[1], self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)

	def update(self, surface, chunks_list, deltaTime, camera, test=False):

		self.camera_updater(Camera=camera)
		self.update_screen_pos()
		self.update_hitbox()

		if self.__isEntityOnScreen__():
			self.Enable_Physics()
		else:
			self.Disable_Phyisics()

		if mg.Pause == False:
			if self.EnablePhysics:
				collided_blocks = self.nearbyblocks(chunks_list)
				self.physics(collided_blocks, surface, deltaTime=deltaTime)
				self.update_pos()

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
		self.body_shape(surface, tuple(self.screen_pos), 0)
		self.DrawTag(surface)
		#pygame.draw.rect(surface, (255,0,0), pygame.Rect( ( self.screen_pos[0], self.screen_pos[1], self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff) ))


	def nearbyblocks(self, chunks_list):
		# This causes certain lag

		# Between all the blocks from the screen detect the ones that are closer to the player
		increaseSize = 100
		biggerHitbox = ( # Make the entity hitbox bigger to detect the surrounding blocks
					self.hitbox[0] - increaseSize//2,
					self.hitbox[1] - increaseSize//2,
					self.hitbox[2] + increaseSize,
					self.hitbox[3] + increaseSize
		)

		output = []
		for c in range(len(chunks_list)): # Active chunks
			for i in range(len(chunks_list[c]["BLOCKS"])): # Blocks from each chunk
				if chunks_list[c]["BLOCKS"][i].coll_hitbox2(pygame.Rect(biggerHitbox)):
					output.append(chunks_list[c]["BLOCKS"][i])
					chunks_list[c]["BLOCKS"][i].setglow(True)
		
		return output
			

	def physics(self, every_block_list, surface, deltaTime=1):
		self.oneList = every_block_list
				
		# Gravity 
		self.vel_y += (1 * deltaTime)
		if self.vel_y > gravity:
			self.vel_y = gravity

		self.dy += (self.vel_y * (deltaTime))
		
		self.player_hitbox = pygame.Rect(self.hitbox)
		self.screen_entity_hitbox = (self.screen_pos[0], self.screen_pos[1], self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)

		self.collitions_ready = [False, False] # Collition x and y

		# Check collition
		for c in range(len(self.oneList)):
			self.block = self.oneList[c]
			self.block_pos = self.oneList[c].getGridCoords()
			self.block_hitbox = pygame.Rect(self.oneList[c].getHitbox())

			if self.block.blockDetection():
				
				x_formula = (self.screen_pos[0]+ self.dx, self.screen_pos[1] , self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)

				# X collition
				if self.block.coll_hitbox( pygame.Rect(x_formula), undetectable_ids=[0] ) and not self.collitions_ready[0]:
					done = False
					if self.dx > 0:
						resting = 0
						for resting in range(self.vel):
							self.entity_hitbox_test = (self.screen_entity_hitbox[0] - (resting - (5*deltaTime)), self.screen_entity_hitbox[1], self.screen_entity_hitbox[2], self.screen_entity_hitbox[3])
							if not self.block.coll_hitbox( pygame.Rect(self.entity_hitbox_test), undetectable_ids=[0] ):
								self.dx -= (resting + 5*deltaTime)
								done = True
								break

							
					elif self.dx < 0:
						done = False
						resting = 0
						for resting in range(self.vel):
							self.entity_hitbox_test = (self.screen_entity_hitbox[0] + (resting - 5*deltaTime), self.screen_entity_hitbox[1], self.screen_entity_hitbox[2], self.screen_entity_hitbox[3])
							if not self.block.coll_hitbox( pygame.Rect(self.entity_hitbox_test), undetectable_ids=[0] ):
								self.dx += (resting + 5*deltaTime)
								done = True
								break


					if not done:
						self.dx = 0

					self.collitions_ready[0] = True

					
					
				y_formula = (self.screen_pos[0], self.screen_pos[1] + self.dy, self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)
				# Y collition
				if self.block.coll_hitbox( pygame.Rect(y_formula), undetectable_ids=[0] ):

					# Check if its under the ground
					if self.dy < 0:
						self.dy = (self.block.getHitbox().bottom) - pygame.Rect(self.screen_entity_hitbox).top
						self.vel_y = 0

					elif self.dy >= 0:

						self.dy = (self.block.getHitbox().top) - pygame.Rect(self.screen_entity_hitbox).bottom

						self.jumping = False
				
				"""pygame.draw.rect(surface, (0,0,255), pygame.Rect(x_formula))
				pygame.draw.rect(surface, (255,0,0), pygame.Rect(y_formula))"""
			

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
		return self.CameraMain.convert_screen_pos_to_camera_xy((self.screen_pos[0], self.screen_pos[1]))

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
			self.vel_y = -12
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

		
		

		

		
