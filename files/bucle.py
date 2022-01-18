import pygame
import sys 
from pygame.locals import *


########## LOCAL MODULES ##########
from files.vars import mouse_hitbox, fps, Frames_per_second, Playing, win
import files.draw as dr

	
def bucle():
	global mouse_hitbox, deltaTime, FPS

	while Playing == True:
		
		events = pygame.event.get()

		# Mouse's hitbox
		mouse_hitbox.left, mouse_hitbox.top = pygame.mouse.get_pos()

		# Frames per second
		FPS = fps.tick(Frames_per_second)

		#DeltaTime
		deltaTime = FPS/15

		Events(events)

		update(events)

def Events(events):
	global Playing, DebugScreen

	for event in events:

		if event.type == QUIT:
			Playing = False
			print("Exit")
			sys.exit()
		
		elif event.type == pygame.KEYDOWN:
			if event.key == K_F3:
				if dr.DebugScreen:
					dr.DebugScreen = False
				else:
					dr.DebugScreen = True
			
def update(events):
	# Clear screen
	win.fill((0,0,0))

	# Draw on screen
	dr.Draw(events)

	# Update each frame
	pygame.display.flip()