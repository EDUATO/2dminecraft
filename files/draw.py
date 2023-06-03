import pygame
from pygame.locals import *
import threading

import files.Game as mg
from files.vars import Scene
from files.terrain.terrain_generator import generate, seed, generation_loop, chunk_manager_list,initial_variables, reset_chunk_man_list
from files.menu.gameMenu import GameMenu

mainMenu = GameMenu()

initialChunksGenerated = False

Game_Main_Class = None

threads_running = 0

loop = threading.Thread(target=generation_loop)
def Draw(App):
	global initialChunksGenerated, loop, threads_running
	
	if Scene == "game":
		if chunk_manager_list != []:
			if not loop.is_alive():
				loop = threading.Thread(target=lambda:generation_loop(App))
				try:
					loop.start()
				except RuntimeError: print("Can't generate new chunk, out of memory")

		App.Game_Main_Class.update(App, running_threads_amount=threads_running)
		
		threads_running = threading.active_count()

	elif Scene == "main_menu":
		mainMenu.show(App.surface)

	for event in App.events:
		if event.type == pygame.KEYDOWN:
			if event.key == K_r:
				reset_chunk_man_list()
				initial_variables()
				App.Game_Main_Class = mg.Game(App)