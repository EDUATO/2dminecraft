import pygame
import pygame.locals

Version = ""

Playing = 1

########### WINDOW ###########
modeX = 1080
modeY = 720

flags =  pygame.DOUBLEBUF

win = pygame.display.set_mode((modeX,modeY))

pygame.display.set_caption("Programa") # Win's name

fps = pygame.time.Clock()

Frames_per_second = 60

# Mouse hitbox
mouse_hitbox = pygame.Rect((0,0), (1,1))

# BLOCK SCALE
block_scale_buff = 3

block_to_put_id = 1

gravity = 8

chunk_size = (32, 64)
block_size = 16

slot_size = 16

# Debug
DebugScreen = False

Pause = False


########## SCENE ############
Scene = 0

######### ANIMATION #########


