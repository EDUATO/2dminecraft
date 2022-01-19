import pygame
import files.functions as f
from files.fonts import *
from files.vars import modeX, modeY

pauseBackground = pygame.Surface((modeX, modeY))

pauseBackground.fill((0,0,0))

pauseBackground.set_alpha(125)

def PauseMenu(surface):
	surface.blit(pauseBackground, (0,0))

	f.text(surface, "Game paused", 10, 10, Arial_30, (255,255,255)) 