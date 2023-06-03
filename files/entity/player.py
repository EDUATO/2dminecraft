import pygame, math

from files.vars import block_scale_buff
from files.entity.entity import Entity
from files.functions import convert_blocks_pos_to_camera_xy

class Player(Entity):
	def __init__(self, App, texture, block_pos, Camera, custom_uuid=False, physics=True, bot=False):
	
		self.camera_updater(Camera)

		self.initial_pos = list(block_pos)
		
		self.block_pos = self.initial_pos

		self.pos = list(convert_blocks_pos_to_camera_xy(grid_pos=(-self.block_pos[0], -self.block_pos[1])))

		self.body_parts = {
			"Head" : (0,0,8,8),
			"Head2" : (8,0,8,8),
			"Leg" : (0,8,4,12),
			"Body" : (4, 8, 4, 12),
			"Front_Body" : (12, 8, 8, 12),
			"Arm" : (8, 8, 4, 12),
			"Front_Arm" : (28, 8, 4, 12)
		}
		super().__init__(
			App=App, pos=self.block_pos,  texture=texture, hitbox_size=(8, 32), camera=Camera, body_parts=self.body_parts, 
			entity_scale_buff=block_scale_buff, custom_uuid=custom_uuid, physics=physics)

		# Crop separated body parts
		self.crop_body_pieces()

		self.head_rotation = 0
		
		self.r = pygame.Rect(10000, -1360, 50, 50)

	def get_angle_from_player_to_cursor(self):
		mouse_pos = pygame.mouse.get_pos()

		ady = abs(self.screen_pos[0] - mouse_pos[0])
		opu = abs(self.screen_pos[1] - mouse_pos[1])

		try:
			self.head_rotation = math.atan(opu / ady) * (180 / math.pi)
		except ZeroDivisionError:
			self.head_rotation = 0
		print("ady", ady, ".  opu   ",opu, "angl", self.head_rotation)

	def body_shape(self,surface, pos, state=0):
		self.screen_pos = self.get_screen_pos()

		if state == 0:
			#self.get_angle_from_player_to_cursor()
			#print(self.head_rotation)
			#rotated = pygame.transform.rotate(self.head2, self.head_rotation)
			surface.blit(self.head2, (pos)) # Head

			surface.blit(self.arm1, (self.screen_pos[0] + self.resized_body_parts["Head2"][2]/4 ,self.screen_pos[1] + self.resized_body_parts["Head2"][3])) # Right hand

			surface.blit(self.body, (self.screen_pos[0] + self.resized_body_parts["Head2"][2]/4 ,self.screen_pos[1] + self.resized_body_parts["Head2"][3])) # Body

			surface.blit(self.arm2, (self.screen_pos[0] + self.resized_body_parts["Head2"][2]/4 ,self.screen_pos[1] + self.resized_body_parts["Head2"][3])) # Right hand

			surface.blit(self.leg1, (self.screen_pos[0] + self.resized_body_parts["Head2"][2]/4 ,self.screen_pos[1] + self.resized_body_parts["Head2"][3] + self.resized_body_parts["Body"][3])) # Leg 1

			surface.blit(self.leg2, (self.screen_pos[0] + self.resized_body_parts["Head2"][2]/4 ,self.screen_pos[1] + self.resized_body_parts["Head2"][3] + self.resized_body_parts["Body"][3])) # Leg 2


		elif state == 1:
			surface.blit(self.head1, (self.screen_pos)) # Head

			surface.blit(self.Front_Body, (self.screen_pos[0] ,self.screen_pos[1] + self.resized_body_parts["Head"][3])) # Body

			surface.blit(self.leg1, (self.screen_pos[0] ,self.screen_pos[1] + self.resized_body_parts["Head"][3] + self.resized_body_parts["Front_Body"][3])) # Leg 1

			surface.blit(self.leg2, (self.screen_pos[0] + self.resized_body_parts["Leg"][2] ,self.screen_pos[1] + self.resized_body_parts["Head"][3] + self.resized_body_parts["Front_Body"][3])) # Leg 2

			surface.blit(self.Front_Arm1, (self.screen_pos[0] + self.resized_body_parts["Front_Body"][2] ,self.screen_pos[1] + self.resized_body_parts["Head2"][3])) # Right hand

			surface.blit(self.Front_Arm2, (self.screen_pos[0] - self.resized_body_parts["Front_Arm"][2] ,pself.screen_posos[1] + self.resized_body_parts["Head2"][3])) # Left hand
	def keyMovement(self, deltaTime):
		
		self.keys = pygame.key.get_pressed()

		if self.keys[pygame.K_d]:
			if not self.keys[pygame.K_a] == 1:
				self.move(direction="R", deltaTime=deltaTime)
				
		if self.keys[pygame.K_a]:
			if not self.keys[pygame.K_d] == 1:
				self.move(direction="L", deltaTime=deltaTime)

		if self.keys[pygame.K_SPACE]:
			self.move(direction="U", deltaTime=deltaTime)

		# FOR TESTING PURPOSES ONLY
		if self.keys[pygame.K_w]:
			if not self.keys[pygame.K_s] == 1:
				self.move(direction="W", deltaTime=deltaTime)

		if self.keys[pygame.K_s]:
			if not self.keys[pygame.K_w] == 1:
				self.move(direction="S", deltaTime=deltaTime)

	def crop_body_pieces(self):
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



