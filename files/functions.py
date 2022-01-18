import pygame

########## LOCAL MODULES ##########
from files.vars import win

def text(txt,x, y, FUENTE, COLOR):
	text.Text = FUENTE.render(txt,1,(COLOR))
	win.blit(text.Text,(x,y))