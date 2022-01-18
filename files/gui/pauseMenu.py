import pygame
import files.functions as f
from files.fonts import *
from files.vars import modeX, modeY, win

pauseBackground = pygame.Surface((modeX, modeY))

pauseBackground.fill((0,0,0))

pauseBackground.set_alpha(125)

def PauseMenu():
	win.blit(pauseBackground, (0,0))

	f.text("Game paused", 10, 10, Arial_30, (255,255,255)) 