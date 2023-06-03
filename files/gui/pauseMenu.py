import pygame

from files.vars import modeX, modeY
from files.gui.Text import Text

pauseBackground = pygame.Surface((modeX, modeY))

pauseBackground.fill((0,0,0))

pauseBackground.set_alpha(125)

crop = (0,132,200*2,20*2)

def PauseMenu(App):
	App.surface.blit(pauseBackground, (0,0))
	
	App.surface.blit(App.assets.Widgets_texture, (170,5), crop)
	PauseText = Text(230, 15, "Game Paused", App.assets.Mc_15, (255,255,255))
	PauseText.draw(App)

	