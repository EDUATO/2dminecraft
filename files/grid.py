import pygame

from files.vars import win, block_scale_buff, modeX, modeY, camera_coords

def grid(block_size, color):
	for i in range(modeX + int(camera_coords[0])// (block_size * block_scale_buff)):
		pygame.draw.line(win, color, ((16 * block_scale_buff)*(i+1) + camera_coords[0], 0), ((block_size * block_scale_buff)*(i+1) + camera_coords[0], modeY))

	for i in range(modeY + int(camera_coords[1])// (block_size * block_scale_buff)):
		pygame.draw.line(win, color, (0, ((block_size * block_scale_buff) * (i+1) + camera_coords[1])), (modeX, (block_size * block_scale_buff) * (i+1) + camera_coords[1]))