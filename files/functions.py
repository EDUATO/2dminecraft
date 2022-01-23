import pygame
from files.vars import modeX, modeY, block_scale_buff, block_size

########## LOCAL MODULES ##########

def text(surface, txt,x, y, FUENTE, COLOR):
	text.Text = FUENTE.render(txt,1,(COLOR))
	surface.blit(text.Text,(x,y))

def Lock_to(lock, x, y, width, height, screen_areas=(0, 0, modeX, modeY)):

	if lock == "x":
		return ( x + screen_areas[2]/2 - width/2 , y)

	elif lock == "y":
		return (x, y + screen_areas[3]/2 - height/2 )

	elif lock == "xy":
		return (x + screen_areas[2]/2 - width/2, y + screen_areas[3]/2 - height/2 )

	elif lock == "right-top-corner":
		pass

	elif lock == "left-top-corner":
		pass

	return 0

def toNegative(_tuple):
	output = []
	for i in range(len(_tuple)):
		output.append(-(_tuple[i]))

	return output

def isSpriteOnTheScreen(camera:tuple, screenSize:tuple, hitboxSize:tuple):
	if (camera[0] >= (0 - (hitboxSize[0])) and camera[0] <= screenSize[0] + (hitboxSize[0]) and (camera[1] >= (0 - (hitboxSize[1]) ) and camera[1] <= screenSize[1] + (hitboxSize[1]) )):
		return True

def convert_blocks_pos_to_camera_xy(grid_pos:tuple, block_size=(block_size*block_scale_buff)):
	return (-(grid_pos[0] * block_size), (grid_pos[1] * block_size))

def convert_camera_xy_to_block_pos(xy_pos:tuple, block_size=(block_size*block_scale_buff)):
	return ((xy_pos[0] / block_size), -(xy_pos[1] / block_size))