import pygame

if __name__ == "__main__":
	from vars import modeX, modeY, block_scale_buff, block_size
else:
	from files.vars import modeX, modeY, block_scale_buff, block_size

########## LOCAL MODULES ##########

def Lock_to(lock, x, y, width, height, screen_areas=(0, 0, modeX, modeY)):

	if lock == "x":
		return ( x + screen_areas[2]/2 - width/2 , y)

	elif lock == "y":
		return (x, y + screen_areas[3]/2 - height/2 )

	elif lock == "xy":
		return (x + screen_areas[2]/2 - width/2, y + screen_areas[3]/2 - height/2 )

	return 0

def toNegative(_tuple):
	output = []
	for i in range(len(_tuple)):
		output.append(-(_tuple[i]))

	return output

def isSpriteOnTheScreen(cameraSize:tuple, screenHitbox:pygame.Rect, startCameraPos=(0,0)):
	""" screenHitbox has to be pygame.Rect object """
	return pygame.Rect((startCameraPos[0], startCameraPos[1], cameraSize[0], cameraSize[1])).colliderect(screenHitbox)

def convert_blocks_pos_to_camera_xy(grid_pos:tuple, block_size=(block_size*block_scale_buff)):
	return (-(grid_pos[0] * block_size), (grid_pos[1] * block_size))

def convert_screen_pos_to_camera_xy(screen_pos):
	return (-(screen_pos[0]), screen_pos[1])

def convert_camera_xy_to_block_pos(xy_pos:tuple, block_size=(block_size*block_scale_buff)):
	return (-(xy_pos[0] / block_size), (xy_pos[1] / block_size))

def lined_rect(surface, rect:pygame.Rect, color, width_line):
	# Horizontals
	pygame.draw.line(surface, color, (rect.x , rect.y), (rect.width, rect.y), width_line)
	pygame.draw.line(surface, color, (rect.x, rect.height), (rect.width, rect.height), width_line)

	# Verticals
	pygame.draw.line(surface, color, (rect.x, rect.y), (rect.x, rect.height), width_line)
	pygame.draw.line(surface, color, (rect.width, rect.y), (rect.width, rect.height), width_line)

if __name__ == "__main__":
	a = (-5.0, -15.985)

	print(a)

	a_block = convert_blocks_pos_to_camera_xy(grid_pos=a)

	print(a_block)

	a_again = convert_camera_xy_to_block_pos(a_block)

	print(a_again)