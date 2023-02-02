import pygame
from files.vars import block_scale_buff
from files.import_imp import Blocks_texture

block_texture = pygame.transform.scale(Blocks_texture, (Blocks_texture.get_width() * block_scale_buff,  Blocks_texture.get_height() * block_scale_buff)) # To the spritesheet

every_block_list = { # This contains every texture block id
	0 : { "Name" : "Air", "crop" : None},
	1 : { "Name" : "Grass_Block", "crop" : (0,0,16,16)},
	2 : { "Name" : "Stone_Block", "crop" : (16,0,16,16)},
	3 : { "Name" : "Dirt", "crop" : (32,0,16,16)},
	4 : { "Name" : "Bedrock", "crop" : (64,0,16,16)},
	5 : { "Name" : "Wood", "crop": (48,0,16,16)},
	6 : { "Name" : "Leaves", "crop": (160,0,16,16)},
	7 : { "Name" : "tree", "crop": (110,0,16,16)},
	8 : { "Name" : "house", "crop": (69,0,16,16)},
	9 : { "Name" : "wooden planks", "crop": (96,0,16,16)},
	10 : { "Name" : "Stone Bricks", "crop": (144,0,16,16)},
	11 : { "Name" : "Chest", "crop": (176,0,16,16)}
	
	}