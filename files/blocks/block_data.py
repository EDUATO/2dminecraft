from files.blocks.every_block_data import every_block_list

from files.blocks.air import *
from files.blocks.dirt import *
from files.blocks.grass_block import *
from files.blocks.stone import *
from files.blocks.bedrock import *
from files.blocks.wood import *
from files.blocks.leaves import *
from files.blocks.gen_tree import *
from files.blocks.gen_house import *
from files.blocks.wooden_planks import *
from files.blocks.stone_bricks import *
from files.blocks.chest import *

placeble_blocks_list = {
	0 : {"Name" : "Air", "class" : Air()},
	1 : {"Name" : "Grass_Block", "class" : Grass_Block()},
	2 : {"Name" : "Stone_Block", "class" : Stone()},
	3 : {"Name" : "Dirt", "class" : Dirt()},
	4 : {"Name" : "Bedrock", "class" : Bedrock()},
	5 : {"Name" : "Wood", "class": Wood()},
	6 : {"Name" : "Leaves", "class": Leaves()},
	7 : {"Name" : "Gen-Tree", "class": Tree()},
	8 : {"Name" : "Gen-House", "class": House()},
	9 : {"Name" : "Woodenplanks", "class": WoodenPlanks()},
	10 : {"Name" : "Stone Bricks", "class": StoneBricks()},
	11 : {"Name" : "Chest", "class": Chest()}
	
}

