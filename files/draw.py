import pygame

import files.Game as mg
from files.vars import Scene
from files.fonts import *
from files.gui.pauseMenu import PauseMenu

def Draw(events):
	if Scene == 0:
		mg.game(events=events)

		if mg.Pause:
			PauseMenu()