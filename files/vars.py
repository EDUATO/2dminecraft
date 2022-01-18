import pygame
import pygame.locals

Version = ""

Playing = True

########### WINDOW ###########
modeX = 1080
modeY = 720

flags = None

win = pygame.display.set_mode( (modeX,modeY) )

pygame.display.set_caption("Programa") # Win's name

fps = pygame.time.Clock()

Frames_per_second = 60

# Mouse hitbox
mouse_hitbox = pygame.Rect((0,0), (0,0))

block_scale_buff = 1

block_to_put_id = 1

camera_coords = [0,0]


########## SCENE ############
Scene = 0

######### ANIMATION #########


