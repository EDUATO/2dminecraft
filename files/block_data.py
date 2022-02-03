import pygame
from files.vars import block_scale_buff
from files.import_imp import Blocks_texture

block_texture = pygame.transform.scale(Blocks_texture, (Blocks_texture.get_width() * block_scale_buff,  Blocks_texture.get_height() * block_scale_buff)) # To the spritesheet

every_block_list = { # This contains every block id, inclusive each part of the door
	0 : { "Name" : "Air", "crop" : None, "durability":False},
	1 : { "Name" : "Grass_Block", "crop" : (0,0,16,16), "durability":40},
	2 : { "Name" : "Stone_Block", "crop" : (16,0,16,16), "durability":140},
	3 : { "Name" : "Dirt", "crop" : (32,0,16,16), "durability":35},
	
	}

from files.blocks.air import *
from files.blocks.dirt import *
from files.blocks.grass_block import *
from files.blocks.stone import *

placeble_blocks_list = {
	0 : {"Name" : "Air", "class" : Air()},
	1 : {"Name" : "Grass_Block", "class" : Grass_Block()},
	2 : {"Name" : "Stone_Block", "class" : Stone()},
	3 : {"Name" : "Dirt", "class" : Dirt()}
}





"""
	4 : { "Name" : "Oak_Wood", "crop" : (48,0,16,16), "durability":70},
	5 : { "Name" : "Bedrock", "crop" : (64,0,16,16), "durability":False},
	6 : { "Name" : "Iron Ore", "crop" : (80,0,16,16), "durability":150},
	7 : { "Name" : "Wooden Planks", "crop" : (96,0,16,16), "durability":70},
	8 : { "Name" : "SECRET", "crop" : (64,0,16,16), "durability":4},
	8 : { "Name" : "Door1", "crop" : (112,0,16,16), "durability":70},
	9 : { "Name" : "Door2", "crop" : (128,0,16,16), "durability":70}

"""