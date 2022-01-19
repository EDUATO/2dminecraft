import pygame

import files.Game as mg
from files.vars import Scene
from files.gui.pauseMenu import PauseMenu

def Draw(surface, events):
	if Scene == 0:
		mg.game(events=events, surface=surface)

		if mg.Pause:
			PauseMenu(surface)