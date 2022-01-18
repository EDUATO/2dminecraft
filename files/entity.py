import pygame

from files.import_imp import *
from files.vars import win, block_scale_buff


class Entity:
	def __init__(self, pos, texture, hitbox_size, body_parts, entity_scale_buff=1):
		self.pos = pos
		self.hitbox_size = hitbox_size

		self.texture = texture

		self.entity_scale_buff = entity_scale_buff

		self.player_texture = pygame.transform.scale(self.texture, (self.texture.get_width() * self.entity_scale_buff,  self.texture.get_height() * self.entity_scale_buff)) # To the spritesheet

		self.body_parts = body_parts

		self.resized_body_parts = {}

		self.gravity = 4

		self.body_parts_keys = list(self.body_parts.keys())
		for i in range(len(self.body_parts)):
			self.resized_body_parts[self.body_parts_keys[i]] = [] # Add a list, so you can append info
			for t in range(4):
				self.resized_body_parts[self.body_parts_keys[i]].append(self.body_parts[self.body_parts_keys[i]][t] * self.entity_scale_buff )


	def body_shape(self, pos):
		pass

	def update(self):
		self.hitbox = (self.pos[0], self.pos[1], self.hitbox_size[0] * self.entity_scale_buff, self.hitbox_size[1] * self.entity_scale_buff)

		#pygame.draw.rect(win, (255,255,0), self.hitbox)

		self.body_shape(tuple(self.pos))

		self.physics()

	def physics(self):
		pass

	def get_pos(self):
		return self.pos

	def get_hitbox(self):
		return self.hitbox

