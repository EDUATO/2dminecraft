import pygame

from files.fonts import *
from files.vars import modeX, modeY
from files.gui.Text import Text
from files.import_imp import Widgets_texture

pauseBackground = pygame.Surface((modeX, modeY))

pauseBackground.fill((0,0,0))

pauseBackground.set_alpha(125)

resized_widgets = pygame.transform.scale2x(Widgets_texture)
crop = (0,132,200*2,20*2)

def PauseMenu(surface):
	surface.blit(pauseBackground, (0,0))
	
	surface.blit(resized_widgets, (170,5), crop)
	PauseText = Text(230, 15, "Game Paused", Mc_15, (255,255,255))
	PauseText.draw(surface)

	