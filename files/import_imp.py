import pygame
from pygame.locals import *

########## LOCAL MODULES ########## 


class import_images:

	def __init__(self):
		import_images.images(self)
		
		import_images.audios(self)

		import_images.fonts(self)

	def cropped_images(self):
		global Blocks_texture, Grass
		Blocks_texture = pygame.image.load("sprites/Blocks.png").convert_alpha()


	def images(self):
		# Get crops from cropped images
		import_images.cropped_images(self)

		# Images
		
				
	def audios(self):
		pass

	def fonts(self):
		global Arial

		Arial = "fonts/1.ttf"


import_images()