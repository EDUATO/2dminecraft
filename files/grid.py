import pygame

from files.vars import win, block_scale_buff, modeX, modeY
import files.bucle as b

def grid(block_size, color, camera_coords):
	# Negative coordinates lags the game

	# X
	for i in range(modeX + int(abs(camera_coords[0]))):
		if (int(camera_coords[0]) + modeX) >= 0:
			pygame.draw.line(win, color, ((16 * block_scale_buff)*(-i-1) + camera_coords[0], 0), ((block_size * block_scale_buff)*(-i-1) + camera_coords[0], modeY))
		if (int(camera_coords[0]) - modeX) <= 0:
			pygame.draw.line(win, color, ((16 * block_scale_buff)*(i) + camera_coords[0], 0), ((block_size * block_scale_buff)*(i) + camera_coords[0], modeY))

	# Y
	for i in range(modeY + int(abs(camera_coords[1]))):
		if (int(camera_coords[1]) + modeY) >= 0:
			pygame.draw.line(win, color, (0, ((block_size * block_scale_buff) * (-i-1) + camera_coords[1])), (modeX, (block_size * block_scale_buff) * (-i-1) + camera_coords[1]))
		if (int(camera_coords[1]) - modeY) <= 0:
			pygame.draw.line(win, color, (0, ((block_size * block_scale_buff) * (i) + camera_coords[1])), (modeX, (block_size * block_scale_buff) * (i) + camera_coords[1]))

	#print(camera_coords)