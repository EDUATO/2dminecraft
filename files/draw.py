import pygame
import threading

import files.Game as mg
from files.vars import Scene
from files.gui.pauseMenu import PauseMenu
from files.terrain.terrain_generator import generate, seed, generation_loop, Chunk_Manager_List
from files.menu.gameMenu import GameMenu
from files.saving.gamesave import save

# TERRAIN GENERATOR
loop = threading.Thread(target=generation_loop, daemon=True) # It destroys when the main thread ends
loop.start()

mainMenu = GameMenu()

initialChunksGenerated = False

Game_Main_Class = None

def Draw(surface, events):
	global initialChunksGenerated, Game_Main_Class
	if Scene == "game":
		if initialChunksGenerated:
			Game_Main_Class.update(events, surface)

			if mg.Pause:
				PauseMenu(surface)
				save()

		else:
			if Chunk_Manager_List == []:
				initialChunksGenerated = True
				Game_Main_Class = mg.Game()

	elif Scene == "main_menu":
		mainMenu.show(surface)