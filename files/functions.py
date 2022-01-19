import pygame

########## LOCAL MODULES ##########

def text(surface, txt,x, y, FUENTE, COLOR):
	text.Text = FUENTE.render(txt,1,(COLOR))
	surface.blit(text.Text,(x,y))


def isSpriteOnTheScreen(camera:tuple, screenSize:tuple, hitboxSize:tuple):
	if (camera[0] >= (0 - (hitboxSize[0])) and camera[0] <= screenSize[0] + (hitboxSize[0]) and (camera[1] >= (0 - (hitboxSize[1]) ) and camera[1] <= screenSize[1] + (hitboxSize[1]) )):
		
		
		return True