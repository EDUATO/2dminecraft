import pygame
import threading

import files.Game as mg
from files.vars import Scene
from files.gui.pauseMenu import PauseMenu
from files.terrain.terrain_generator import generate, seed, generation_loop, chunks_list, Chunk_Manager_List

# TERRAIN GENERATOR
loop = threading.Thread(target=generation_loop, daemon=True, args=[mg.CameraMain]) # It destroys when the main thread ends
loop.start()

initialChunksGenerated = False

def Draw(surface, events):
	global initialChunksGenerated
	if Scene == 0:
		if initialChunksGenerated:
			mg.game(events=events, surface=surface)

			if mg.Pause:
				PauseMenu(surface)

		else:
			if Chunk_Manager_List == []:
				initialChunksGenerated = True