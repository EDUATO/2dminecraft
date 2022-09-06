import pygame
import sys 
from pygame.locals import *


########## LOCAL MODULES ##########
from files.vars import mouse_hitbox, fps, Frames_per_second, Playing
import files.draw as dr

FramebyFrame_mode = False

def bucle(surface):
	global mouse_hitbox, deltaTime, FPS
	
	while Playing == 1:
		
		events = pygame.event.get()

		# Mouse's hitbox
		mouse_hitbox.left, mouse_hitbox.top = pygame.mouse.get_pos()

		# Frames per second
		FPS = fps.tick(60)

		#DeltaTime
		deltaTime = FPS/15
		if deltaTime > 10:
			deltaTime = 1

		#deltaTime = 9

		Events(surface, events)

		if not FramebyFrame_mode:
			update(surface, events)
		
def Events(surface, events):
	global Playing, FramebyFrame_mode

	for event in events:

		if event.type == QUIT:
			dr.Game_Main_Class.save_world()
			Playing = 0
			print("Exit")
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == K_F2:
				if FramebyFrame_mode:
					FramebyFrame_mode = False
					pygame.mouse.set_visible(False)
					print("[FramebyFrame] FramebyFrame mode Desactivated!")
				else:
					FramebyFrame_mode = True
					pygame.mouse.set_visible(True)
					print("[FramebyFrame] FramebyFrame mode Activated!")
					print("[FramebyFrame] Use the plus key to go to the following frame")

			elif event.key == K_PLUS:
				if FramebyFrame_mode:
					update(surface, events)
			
			
def update(surface, events):
	# Draw on screen
	dr.Draw(surface, events)

	# Update each frame
	pygame.display.flip()