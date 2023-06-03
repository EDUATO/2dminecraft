import pygame, time
import sys 
from pygame.locals import *


########## LOCAL MODULES ##########
from files.import_imp import import_images
import files.draw as dr
from files.gui.Text import Text 
import files.Game as mg

FramebyFrame_mode = False

prev_time = time.time()

class App:
	def __init__(self, dims:tuple):
		self.pressed_time = 0 # for debug mode
		flags =  pygame.RESIZABLE
		self.surface = pygame.display.set_mode(dims, flags)

		pygame.display.set_caption("App")

		self.fps = pygame.time.Clock()

		self.Frames_per_second = 60
		self.FramebyFrame_mode = False
		self.inProgram = 1
		self.assets = import_images()
		self.deltaTime = 1
		self.prev_time = 0
		# Mouse hitbox
		self.mouse_hitbox = pygame.Rect((0,0), (1,1))

		# Game
		self.Game_Main_Class = mg.Game(self)

	def update(self):
		while self.inProgram:
		
			self.events = pygame.event.get()

			# Mouse's hitbox
			self.mouse_hitbox.left, self.mouse_hitbox.top = pygame.mouse.get_pos()

			# Frames per second
			FPS = self.fps.tick(self.Frames_per_second)

			#DeltaTime
			now_time = time.time()
			self.deltaTime = (now_time - self.prev_time) * 90
			self.prev_time = now_time

			self._events()

			if not FramebyFrame_mode:
				self._draw()

	
	def _events(self):

		for event in self.events:

			if event.type == QUIT:
				self.Game_Main_Class.save_world()
				self.inProgram = 0
				print("Exit")
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == K_F2:
					if self.FramebyFrame_mode:
						self.FramebyFrame_mode = False
						pygame.mouse.set_visible(False)
						print("[FramebyFrame] FramebyFrame mode Desactivated!")
					else:
						self.FramebyFrame_mode = True
						pygame.mouse.set_visible(True)
						print("[FramebyFrame] FramebyFrame mode Activated!")
						print("[FramebyFrame] Use the plus key to go to the following frame")


		keys = pygame.key.get_pressed()

		if keys[K_PLUS]:
			if pressed_time == 0 or pressed_time > 30:
				if self.FramebyFrame_mode:
					update(surface, events)

			pressed_time += 1*deltaTime
		elif not keys[K_PLUS]:
			pressed_time = 0
				
				
		# Draw debug mode on screen
		if self.FramebyFrame_mode:
			Text(x=10, y=modeY-100, txt="[DebugMode]", FUENTE=Mc_12, COLOR=(0,0,200)).draw(self.surface)
			pygame.display.flip()

	def _draw(self):
		# Draw on screen
		dr.Draw(self)

		# Update each frame
		pygame.display.flip()