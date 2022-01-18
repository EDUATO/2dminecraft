import pygame

from files.vars import win, block_scale_buff, modeX, modeY

def grid(block_size, color):
	for i in range(modeX// (block_size * block_scale_buff)):
		pygame.draw.line(win, color, ((16 * block_scale_buff)*(i+1), 0), ((block_size * block_scale_buff)*(i+1), modeY))

	for i in range(modeY// (block_size * block_scale_buff)):
		pygame.draw.line(win, color, (0, ((block_size * block_scale_buff) * (i+1))), (modeX, (block_size * block_scale_buff) * (i+1)))