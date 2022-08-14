import pygame
import threading
import uuid
import random
import pymunk
import pymunk.pygame_util

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

		self.physics_shape = self.create_hitbox_physics_rect()

		self.update_hitbox()
		self._set_physics_position(pos=(540, 260))

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

	def create_hitbox_physics_rect(self):
		block_body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
		block_body.position = (0, 0)
		rect_size = (200, 100)
		#block_body.mass = 100
		shape = pymunk.Poly.create_box(block_body, rect_size)

		shape.color = (100, 100,200, 1)

		return shape

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

		# Physics pos update
		self.dy = 0
		self.dx = 0

		self.jumping = False
		self.jump_vel = 16

	def set_Inventory(self):
		self.EntityInventory = Inventory()
		self.EntityHotbar = Hotbar()

	def update_hitbox(self):
		self.hitbox = (self.screen_pos[0] + self.dx, self.screen_pos[1] + self.dy, self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)
		

	def update(self, surface, chunks_list, deltaTime, camera, test=False):
		#self.physics_body = self.create_hitbox_physics_rect()
		#print(self.shape.body.position)
		self.camera_updater(Camera=camera)
		self.update_screen_pos()
		
		
		#print(f"{self.physics_body[0].position.x}, {self.physics_body[0].position.y}")
		if self.__isEntityOnScreen__():
			self.Enable_Physics()
		else:
			self.Disable_Phyisics()

		self.update_hitbox()

		if self.EnablePhysics:
			self.update_pos()
			self.update_hitbox()
			
		self.Draw(surface)

		self.dx = 0
		self.dy = 0

		if test:
			self.Automate(deltaTime)

	def _set_physics_position(self, pos:tuple): 
		#self.physics_shape.body._set_position(pos=(int(pos[0]), int(pos[1])))
		self.physics_shape.body._set_position(pos=(int(pos[0]), int(pos[1])))

	def updateInventory(self, surface, events, mouse, keys):
		self.EntityInventory.update(surface, mouse, keys)
		self.EntityHotbar.update(events, surface, Inventory_slots=self.EntityInventory.getInventorySlots())
	
	def getEntityHotbar(self):
		return self.EntityHotbar

	def Draw(self, surface):
		draw_formula = (self.screen_pos[0], self.screen_pos[1], self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)

		self.body_shape(surface, tuple(draw_formula), 0)
		self.DrawTag(surface)
		#pygame.draw.rect(surface, (255,0,0), pygame.Rect( ( self.screen_pos[0], self.screen_pos[1], self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff) ))
		

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

	def get_physics_shape(self): return self.physics_shape

	def move(self, deltaTime, direction=None):
		self.jumping = False
		if direction == "R":
			self.dx += (self.vel * deltaTime)
			
		if direction == "L":
			self.dx -= (self.vel * deltaTime)

		if direction == "U":
			self.dy -= (self.vel * deltaTime)

		if direction == "S":
			self.dy += (self.vel * deltaTime)

		"""if direction == "U" and self.jumping == False:
			self.vel_y = -self.jump_vel
			self.jumping = True"""

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

		
		

		

		
