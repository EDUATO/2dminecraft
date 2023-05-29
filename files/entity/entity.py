import pygame
import threading
import uuid
import random

from files.import_imp import *
from files.fonts import *
from files.vars import gravity
from files.blocks.Block import *
import files.mainLoop as b
import files.Game as mg
from files.functions import convert_blocks_pos_to_camera_xy, convert_camera_xy_to_block_pos
from files.gui.hotbar import Hotbar
from files.gui.Inventory import Inventory
from files.gui.Text import Text
from files.physics import Physics

class Entity:
	def __init__(self, pos, texture, hitbox_size, camera, body_parts, custom_uuid=False, entity_scale_buff=2, physics=True, bot=False):
		self.block_pos = pos # The position is in blocks
		self.pos = list(convert_blocks_pos_to_camera_xy(grid_pos=(-self.block_pos[0], -self.block_pos[1])))
		self.canMove = True

		if custom_uuid:
			self.entity_uuid = custom_uuid
		else:
			self.entity_uuid = uuid.uuid4()

		self.camera_updater(Camera=camera)

		self.update_screen_pos()

		self.BOT = bot

		self.texture = texture

		self.entity_scale_buff = entity_scale_buff

		self.hitbox_size = (hitbox_size[0] * self.entity_scale_buff, hitbox_size[1] * self.entity_scale_buff)

		self.player_texture = pygame.transform.scale(self.texture, (self.texture.get_width() * self.entity_scale_buff,  self.texture.get_height() * self.entity_scale_buff)) # To the spritesheet

		self.body_parts = body_parts

		self.show_tag = True

		self.resized_body_parts = {}

		self.initialize_physics(physics)

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
		EntityTag = Text(txt="bob-"+str(self.entity_uuid), x=self.screen_pos[0], y=self.screen_pos[1]-20, FUENTE=Mc_12, COLOR=(255,0,0),lock="x",
					 	screen_areas=(self.screen_pos[0], self.screen_pos[1]-20, self.hitbox_size[0], self.screen_pos[1]-20))

		EntityTag.draw(surface=surface)

	def initialize_physics(self, physics:bool):
		self.EnablePhysics = physics

		self.vel = 10

		self.jumping = False
		self.jump_vel = 16

		self.EntityPhysics = Physics(
			hitbox_size=self.hitbox_size
		)

	def set_Inventory(self):
		self.EntityInventory = Inventory()
		self.EntityHotbar = Hotbar()

	def update_hitbox(self):
		self.hitbox = (self.screen_pos[0] + self.EntityPhysics.return_dx, self.screen_pos[1] + self.EntityPhysics.dy, self.hitbox_size[0], self.hitbox_size[1])

	def update(self, surface, chunks_list, deltaTime, camera):

		self.camera_updater(Camera=camera)
		self.update_screen_pos()
		
		self.Enable_Physics()
		self.entity_can_move(True)
		"""if self.__isEntityOnScreen__():
			self.Enable_Physics()
			self.entity_can_move(True)
		else:
			self.Disable_Phyisics()
			self.entity_can_move(False)"""

		self.update_hitbox()

		if self.EnablePhysics:
			self.EntityPhysics.update(chunks_list=chunks_list, surface=surface, screen_pos=self.screen_pos, deltaTime=deltaTime)
			self.update_pos()
			self.update_hitbox()
			if self.BOT:
				self.Automate(deltaTime)

		self.Draw(surface)

		

	def updateInventory(self, surface, events, mouse, keys):
		self.EntityInventory.update(surface, mouse, keys)
		self.EntityHotbar.update(events, surface, Inventory_slots=self.EntityInventory.getInventorySlots())
	
	def getEntityHotbar(self):
		return self.EntityHotbar

	def Draw(self, surface):
		#if self.__isEntityOnScreen__():
		draw_formula = (self.screen_pos[0], self.screen_pos[1], self.hitbox_size[0], self.hitbox_size[1])

		self.body_shape(surface, tuple(draw_formula), 0)
		if self.show_tag:
			self.DrawTag(surface)
		
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
		self.pos[0] += self.EntityPhysics.return_dx
		#print(f"e{self.EntityPhysics.dx}")
		self.pos[1] += self.EntityPhysics.dy

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
		if self.canMove:
			self.jumping = False
			if direction == "R":
				self.EntityPhysics.move_x(force=(self.vel * deltaTime))				
			if direction == "L":
				self.EntityPhysics.move_x(force= -(self.vel * deltaTime))	

			if direction == "U" and self.jumping == False:
				self.EntityPhysics.vel_y = -self.jump_vel
				self.jumping = True

	def Automate_Init(self):
		self.move_time = 0
		self.Adir = "R"
	def Automate(self, deltaTime):
		pass

	def entity_can_move(self, status:bool): self.canMove=status

	def __isEntityOnScreen__(self):
		#print(self.screen_pos)
		return isSpriteOnTheScreen(cameraSize=self.camera_size, screenHitbox=pygame.Rect((self.screen_pos[0], self.screen_pos[1], self.hitbox[2], self.hitbox[3])))