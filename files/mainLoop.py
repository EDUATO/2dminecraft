import pygame, time
import sys 
from pygame.locals import *


########## LOCAL MODULES ##########
from files.vars import mouse_hitbox, fps, Frames_per_second, Playing, modeY
import files.draw as dr
from files.gui.Text import Text 
from files.fonts import Mc_12

FramebyFrame_mode = False

prev_time = time.time()

def mainLoop(surface):
	global mouse_hitbox, deltaTime, FPS, pressed_time, prev_time
	
	pressed_time = 0 # for debug mode

	while Playing:
		
		events = pygame.event.get()

		# Mouse's hitbox
		mouse_hitbox.left, mouse_hitbox.top = pygame.mouse.get_pos()

		# Frames per second
		FPS = fps.tick(60)

		#DeltaTime
		now_time = time.time()
		deltaTime = (now_time - prev_time) * 90
		prev_time = now_time

		Events(surface, events)

		if not FramebyFrame_mode:
			update(surface, events)
		
def Events(surface, events):
	global Playing, FramebyFrame_mode, pressed_time

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


	keys = pygame.key.get_pressed()

	if keys[K_PLUS]:
		if pressed_time == 0 or pressed_time > 30:
			if FramebyFrame_mode:
				update(surface, events)

		pressed_time += 1*deltaTime
	elif not keys[K_PLUS]:
		pressed_time = 0
			
			
	# Draw debug mode on screen
	if FramebyFrame_mode:
		Text(x=10, y=modeY-100, txt="[DebugMode]", FUENTE=Mc_12, COLOR=(0,0,200)).draw(surface)
		pygame.display.flip()

def update(surface, events):
	# Draw on screen
	dr.Draw(surface, events)

	# Update each frame
	pygame.display.flip()