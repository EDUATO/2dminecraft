import pygame
import pygame.locals
from files.vars import win
from files. bucle import bucle
########## LOCAL MODULES ##########


def WindowThread():
    from threading import Thread

    def open_window(): 
        from files.bucle import bucle
        from files.vars import win
        bucle(surface=win)

    t = Thread(target=open_window)
    t.start()


if __name__ == "__main__":
    bucle(surface=win)