import pygame, random

from files.import_imp import *
from files.vars import block_scale_buff
from files.entity.entity import Entity
import files.mainLoop as b

class Wty(Entity):
	def __init__(self, texture, pos, Camera, custom_uuid=False, physics=True, bot=False):
	
		self.camera_updater(Camera)

		self.initial_pos = list(pos)
		
		self.pos = self.initial_pos

		self.body_parts = {
			"Head" : (0,0,8,8),
			"Head2" : (8,0,8,8),
			"Body" : (0, 8, 4, 8)
		}
		print(self.pos)
		super().__init__(
			pos=self.pos,  texture=texture, hitbox_size=(8, 32), camera=Camera, body_parts=self.body_parts, 
			entity_scale_buff=block_scale_buff, custom_uuid="Bob", physics=physics)

		# Crop separated body parts
		self.crop_body_pieces()

		self.BOT = True
		

	def body_shape(self,surface, pos, state=0):
		if state == 0:
			surface.blit(self.head1, (pos)) # Head

			surface.blit(self.body, (pos[0] + self.resized_body_parts["Head"][2]/2 - self.resized_body_parts["Body"][2]/2, pos[1] + self.resized_body_parts["Head"][3])) # Body

			surface.blit(self.head2, (pos[0] ,pos[1] + self.resized_body_parts["Head"][3] + self.resized_body_parts["Body"][3])) # Right hand

			

	def keyMovement(self, deltaTime):
		
		self.keys = pygame.key.get_pressed()

		if self.keys[K_d]:
			if not self.keys[K_a] == 1:
				self.move(direction="R", deltaTime=deltaTime)
				
		if self.keys[K_a]:
			if not self.keys[K_d] == 1:
				self.move(direction="L", deltaTime=deltaTime)

		if self.keys[K_SPACE]:
			self.move(direction="U", deltaTime=deltaTime)

		# FOR TESTING PURPOSES ONLY
		if self.keys[K_w]:
			if not self.keys[K_s] == 1:
				self.move(direction="W", deltaTime=deltaTime)

		if self.keys[K_s]:
			if not self.keys[K_w] == 1:
				self.move(direction="S", deltaTime=deltaTime)

	def crop_body_pieces(self):
		self.head1 = self.player_texture.subsurface((self.resized_body_parts["Head"]))

		self.head2 = self.player_texture.subsurface((self.resized_body_parts["Head2"]))

		self.body = self.player_texture.subsurface((self.resized_body_parts["Body"]))

	def Automate(self,deltaTime):
		h = random.randint(1,100)
		self.move_time += 1
		if h > 50:
			self.move(deltaTime, direction="R")
		elif h < 30:
			self.move(deltaTime, direction="L")
		elif h == 45:
			self.move(deltaTime, direction="U")
		else:
			pass



