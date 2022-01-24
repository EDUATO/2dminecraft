import pygame
from files.vars import block_scale_buff
from files.import_imp import Blocks_texture

Blocks_list = {
	0 : { "Name" : "Air", "crop" : None, "durability":False, "special":False },
	1 : { "Name" : "Grass_Block", "crop" : (0,0,16,16), "durability":40, "special":False },
	2 : { "Name" : "Stone_Block", "crop" : (16,0,16,16), "durability":140, "special":False },
	3 : { "Name" : "Dirt", "crop" : (32,0,16,16), "durability":35, "special":False},
	4 : { "Name" : "Oak_Wood", "crop" : (48,0,16,16), "durability":70, "special":False},
	5 : { "Name" : "Bedrock", "crop" : (64,0,16,16), "durability":False, "special":False},
	6 : { "Name" : "Iron Ore", "crop" : (80,0,16,16), "durability":150, "special":False},
	7 : { "Name" : "Wooden Planks", "crop" : (96,0,16,16), "durability":70, "special":False},
	8 : { "Name" : "SECRET", "crop" : (64,0,16,16), "durability":4, "special":False}
	}

Textures_for_blocks_list = {
	0 : { "Name" : "Door1", "crop" : (112,0,16,16), "durability":70},
	1 : { "Name" : "Door2", "crop" : (128,0,16,16), "durability":70}
}

block_texture = pygame.transform.scale(Blocks_texture, (Blocks_texture.get_width() * block_scale_buff,  Blocks_texture.get_height() * block_scale_buff)) # To the spritesheet