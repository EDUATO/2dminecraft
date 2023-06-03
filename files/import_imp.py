import pygame
from pygame.locals import *

from files.vars import block_scale_buff, gui_scale

########## LOCAL MODULES ########## 


class import_images:

	def __init__(self):
		import_images.images(self)
		
		import_images.audios(self)

		import_images.fonts(self)

	def images(self):

		# Images
		self.Blocks_texture = pygame.image.load("sprites/Blocks.png").convert_alpha()
		self.Block_texture_tr = pygame.transform.scale(self.Blocks_texture, (self.Blocks_texture.get_width()*block_scale_buff, self.Blocks_texture.get_height()*block_scale_buff))

		self.Player_texture = pygame.image.load("sprites/player.png").convert_alpha()

		self.Inventory_texture = pygame.image.load("sprites/gui/Inventory.png").convert_alpha()
		self.Inventory_texture_tr = pygame.transform.scale(self.Inventory_texture, (self.Inventory_texture.get_width() * gui_scale,  self.Inventory_texture.get_height() * gui_scale))

		self.Widgets_texture = pygame.image.load("sprites/gui/widgets.png").convert_alpha()

		self.Wty_texture = pygame.image.load("sprites/wty.png").convert_alpha()

		self.Chest_con_texture = pygame.image.load("sprites/gui/chest_container.png").convert_alpha()
		self.Chest_con_texture_tr = pygame.transform.scale(self.Chest_con_texture, (self.Chest_con_texture.get_width() * gui_scale,  self.Chest_con_texture.get_height() * gui_scale))
		
	def audios(self):
		pass

	def fonts(self):
		pygame.font.init()
		Arial = "fonts/1.ttf"
		McFont = "fonts/2.ttf"

		self.Arial_60 = pygame.font.Font(Arial, 60)
		self.Arial_30 = pygame.font.Font(Arial, 30)

		self.Mc_20 = pygame.font.Font(McFont, 20)
		self.Mc_15 = pygame.font.Font(McFont, 15)
		self.Mc_12 = pygame.font.Font(McFont, 12)