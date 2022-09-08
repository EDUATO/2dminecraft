import pygame
from pygame.locals import *
import threading

import files.Game as mg
from files.vars import Scene
from files.terrain.terrain_generator import generate, seed, generation_loop, Chunk_Manager_List,initial_variables, reset_chunk_man_list
from files.menu.gameMenu import GameMenu


mainMenu = GameMenu()

initialChunksGenerated = False

Game_Main_Class = None

def Draw(surface, events):
	global initialChunksGenerated, Game_Main_Class, loop
	if Scene == "game":
		if Chunk_Manager_List != []:
			loop = threading.Thread(target=generation_loop)
			if not loop.is_alive():
				loop.start()


		if initialChunksGenerated and Chunk_Manager_List == []:
			Game_Main_Class.update(events, surface)

		else:
			if Chunk_Manager_List == []:
				initialChunksGenerated = True
				Game_Main_Class = mg.Game()

	elif Scene == "main_menu":
		mainMenu.show(surface)

	for event in events:
		if event.type == pygame.KEYDOWN:
			if event.key == K_r:
				reset_chunk_man_list()
				initial_variables()
				Game_Main_Class = mg.Game()