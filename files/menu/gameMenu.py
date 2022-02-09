import pygame
from files.gui.Text import Text
from files.fonts import *


class GameMenu:
    def __init__(self):
        pass

    def show(self, surface):
        surface.fill((100,140,160))

        hi = Text(10, 10, txt="Hello World", FUENTE=Arial_60, COLOR=(200,200,100), lock="x")

        hi.draw(surface)