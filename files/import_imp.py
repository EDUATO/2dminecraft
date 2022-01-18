import pygame
from pygame.locals import *

########## LOCAL MODULES ########## 


class import_images:

	def __init__(self):
		import_images.images(self)
		
		import_images.audios(self)

		import_images.fonts(self)

	def images(self):
		global Blocks_texture, Player_texture, Inventory_texture, Widgets_texture

		# Images
		Blocks_texture = pygame.image.load("sprites/Blocks.png").convert_alpha()

		Player_texture = pygame.image.load("sprites/player.png").convert_alpha()

		Inventory_texture = pygame.image.load("sprites/gui/Inventory.png").convert_alpha()

		Widgets_texture = pygame.image.load("sprites/gui/widgets.png").convert_alpha()
		
				
	def audios(self):
		pass

	def fonts(self):
		global Arial, McFont

		Arial = "fonts/1.ttf"
		McFont = "fonts/2.ttf"


import_images()