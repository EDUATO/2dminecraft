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

threads_running = None

loop = threading.Thread(target=generation_loop)
def Draw(surface, events):
	global initialChunksGenerated, Game_Main_Class, loop, threads_running
	
	if Scene == "game":
		if chunk_manager_list != []:
			if not loop.is_alive():
				loop = threading.Thread(target=generation_loop)
				try:
					loop.start()
				except RuntimeError: print("Can't generate new chunk, out of memory")

		if initialChunksGenerated and chunk_manager_list == []:
			Game_Main_Class.update(events, surface, running_threads_amount=threads_running)

		else:
			if chunk_manager_list == []:
				initialChunksGenerated = True
				Game_Main_Class = mg.Game()
		threads_running = threading.active_count()

	elif Scene == "main_menu":
		mainMenu.show(surface)

	for event in events:
		if event.type == pygame.KEYDOWN:
			if event.key == K_r:
				reset_chunk_man_list()
				initial_variables()
				Game_Main_Class = mg.Game()