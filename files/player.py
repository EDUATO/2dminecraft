import pygame

from files.import_imp import *
from files.vars import win, block_scale_buff, camera_coords, modeX, modeY
from files.entity import Entity

class Player(Entity):
	def __init__(self, texture, pos):
	
		self.body_parts = {
			"Head" : (0,0,8,8),
			"Head2" : (8,0,8,8),
			"Leg" : (0,8,4,12),
			"Body" : (4, 8, 4, 12),
			"Arm" : (8, 8, 4, 12)
		}
		if pos[0] == "m": # Middle screen
			self.initial_pos = [modeX/2 - 8/2, pos[1]]
		else:
			self.initial_pos = list(pos)
		
		self.pos = self.initial_pos

		super().__init__(self.pos,  texture, (8, 33), self.body_parts, entity_scale_buff=block_scale_buff)

		
		# Crop separated body parts
		self.head2 = self.player_texture.subsurface((self.resized_body_parts["Head2"]))

		self.arm1 = self.player_texture.subsurface((self.resized_body_parts["Arm"]))

		self.arm2 = self.player_texture.subsurface((self.resized_body_parts["Arm"]))

		self.body = self.player_texture.subsurface((self.resized_body_parts["Body"]))

		self.leg1 = self.player_texture.subsurface((self.resized_body_parts["Leg"]))

		self.leg2 = self.player_texture.subsurface((self.resized_body_parts["Leg"]))

	def body_shape(self, pos):

		win.blit(self.head2, (pos)) # Head

		win.blit(self.arm1, (pos[0] + self.resized_body_parts["Head2"][2]/4 ,pos[1] + self.resized_body_parts["Head2"][3])) # Right hand

		win.blit(self.body, (pos[0] + self.resized_body_parts["Head2"][2]/4 ,pos[1] + self.resized_body_parts["Head2"][3])) # Body

		win.blit(self.arm2, (pos[0] + self.resized_body_parts["Head2"][2]/4 ,pos[1] + self.resized_body_parts["Head2"][3])) # Right hand

		win.blit(self.leg1, (pos[0] + self.resized_body_parts["Head2"][2]/4 ,pos[1] + self.resized_body_parts["Head2"][3] + self.resized_body_parts["Body"][3])) # Leg 1

		win.blit(self.leg2, (pos[0] + self.resized_body_parts["Head2"][2]/4 ,pos[1] + self.resized_body_parts["Head2"][3] + self.resized_body_parts["Body"][3])) # Leg 2

	def move(self, events):
		global camera_coords
		self.keys = pygame.key.get_pressed()

		self.camera_limit = modeX
		if self.keys[K_d]:
			if not self.keys[K_a] == 1:
				if self.pos[0] >  modeX - self.camera_limit:
					camera_coords[0] -= 5
				else:
					self.pos[0] += 5
				
		elif self.keys[K_a]:
			if not self.keys[K_d] == 1:
				if self.pos[0] < self.camera_limit:
					camera_coords[0] += 5
				else:
					self.pos[0] -= 5

		elif self.keys[K_s]:
			if not self.keys[K_w] == 1:
				if self.pos[1] > modeY - self.camera_limit/2:
					camera_coords[1] -= 5
				else:
					self.pos[1] += 5

		elif self.keys[K_w]:
			if not self.keys[K_s] == 1:
				if self.pos[1] < self.camera_limit/2:
					camera_coords[1] += 5
				else:
					self.pos[1] -= 5


