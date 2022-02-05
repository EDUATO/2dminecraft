import pygame
import threading

import files.Game as mg
from files.vars import Scene
from files.gui.pauseMenu import PauseMenu
from files.terrain.terrain_generator import generate, seed, generation_loop, chunks_list

# TERRAIN GENERATOR
loop = threading.Thread(target=generation_loop, daemon=True, args=[mg.CameraMain]) # It destroys when the main thread ends
loop.start()

def Draw(surface, events):
	if Scene == 0:
		mg.game(events=events, surface=surface)

		if mg.Pause:
			PauseMenu(surface)