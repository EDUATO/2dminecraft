
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

def get_placeble_blocks_list(App):
	placeble_blocks_list = {
		0 : {"Name" : "Air", "class" : Air(App)},
		1 : {"Name" : "Grass_Block", "class" : Grass_Block(App)},
		2 : {"Name" : "Stone_Block", "class" : Stone(App)},
		3 : {"Name" : "Dirt", "class" : Dirt(App)},
		4 : {"Name" : "Bedrock", "class" : Bedrock(App)},
		5 : {"Name" : "Wood", "class": Wood(App)},
		6 : {"Name" : "Leaves", "class": Leaves(App)},
		7 : {"Name" : "Gen-Tree", "class": Tree(App)},
		8 : {"Name" : "Gen-House", "class": House(App)},
		9 : {"Name" : "Woodenplanks", "class": WoodenPlanks(App)},
		10 : {"Name" : "Stone Bricks", "class": StoneBricks(App)},
		11 : {"Name" : "Chest", "class": Chest(App)}
		
	}
	return placeble_blocks_list

