import pygame

from files.import_imp import *
from files.vars import block_scale_buff
from files.entity import Entity
import files.bucle as b

class Player(Entity):
	def __init__(self, texture, pos, Camera, custom_uuid=False):
	
		self.camera_updater(Camera)

		self.body_parts = {
			"Head" : (0,0,8,8),
			"Head2" : (8,0,8,8),
			"Leg" : (0,8,4,12),
			"Body" : (4, 8, 4, 12),
			"Front_Body" : (12, 8, 8, 12),
			"Arm" : (8, 8, 4, 12),
			"Front_Arm" : (28, 8, 4, 12)
		}

		self.initial_pos = list(pos)
		
		self.pos = self.initial_pos

		super().__init__(self.pos,  texture, (8, 32), Camera, self.body_parts, entity_scale_buff=block_scale_buff, custom_uuid=custom_uuid)

		self.inventory = []

		# Slots
		for y in range(6):
			for x in range(10):
				self.inventory.append({
					"NUM" : (y, x),
					"ITEM" : None
				})
		
		# Crop separated body parts
		self.head1 = self.player_texture.subsurface((self.resized_body_parts["Head"]))

		self.head2 = self.player_texture.subsurface((self.resized_body_parts["Head2"]))

		self.arm1 = self.player_texture.subsurface((self.resized_body_parts["Arm"]))

		self.arm2 = self.player_texture.subsurface((self.resized_body_parts["Arm"]))

		self.body = self.player_texture.subsurface((self.resized_body_parts["Body"]))

		self.Front_Body = self.player_texture.subsurface((self.resized_body_parts["Front_Body"]))

		self.leg1 = self.player_texture.subsurface((self.resized_body_parts["Leg"]))

		self.leg2 = self.player_texture.subsurface((self.resized_body_parts["Leg"]))

		self.Front_Arm1 = self.player_texture.subsurface((self.resized_body_parts["Front_Arm"]))

		self.Front_Arm2 = self.player_texture.subsurface((self.resized_body_parts["Front_Arm"]))

	def body_shape(self,surface, pos, state=0):
		if state == 0:
			surface.blit(self.head2, (pos)) # Head

			surface.blit(self.arm1, (pos[0] + self.resized_body_parts["Head2"][2]/4 ,pos[1] + self.resized_body_parts["Head2"][3])) # Right hand

			surface.blit(self.body, (pos[0] + self.resized_body_parts["Head2"][2]/4 ,pos[1] + self.resized_body_parts["Head2"][3])) # Body

			surface.blit(self.arm2, (pos[0] + self.resized_body_parts["Head2"][2]/4 ,pos[1] + self.resized_body_parts["Head2"][3])) # Right hand

			surface.blit(self.leg1, (pos[0] + self.resized_body_parts["Head2"][2]/4 ,pos[1] + self.resized_body_parts["Head2"][3] + self.resized_body_parts["Body"][3])) # Leg 1

			surface.blit(self.leg2, (pos[0] + self.resized_body_parts["Head2"][2]/4 ,pos[1] + self.resized_body_parts["Head2"][3] + self.resized_body_parts["Body"][3])) # Leg 2

		elif state == 1:
			surface.blit(self.head1, (pos)) # Head

			surface.blit(self.Front_Body, (pos[0] ,pos[1] + self.resized_body_parts["Head"][3])) # Body

			surface.blit(self.leg1, (pos[0] ,pos[1] + self.resized_body_parts["Head"][3] + self.resized_body_parts["Front_Body"][3])) # Leg 1

			surface.blit(self.leg2, (pos[0] + self.resized_body_parts["Leg"][2] ,pos[1] + self.resized_body_parts["Head"][3] + self.resized_body_parts["Front_Body"][3])) # Leg 2

			surface.blit(self.Front_Arm1, (pos[0] + self.resized_body_parts["Front_Body"][2] ,pos[1] + self.resized_body_parts["Head2"][3])) # Right hand

			surface.blit(self.Front_Arm2, (pos[0] - self.resized_body_parts["Front_Arm"][2] ,pos[1] + self.resized_body_parts["Head2"][3])) # Left hand

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



