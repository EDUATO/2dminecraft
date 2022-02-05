import pygame

from files.fonts import *
from files.vars import modeX, modeY
from files.gui.Text import Text

pauseBackground = pygame.Surface((modeX, modeY))

pauseBackground.fill((0,0,0))

pauseBackground.set_alpha(125)

def PauseMenu(surface):
	surface.blit(pauseBackground, (0,0))

	PauseText = Text(10, 10, "Game Paused", Arial_30, (255,255,255))
	PauseText.draw(surface)