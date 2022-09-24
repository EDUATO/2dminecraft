from files.blocks.blocks_man import Blocks_manager
from files.terrain.structure import Structure
from files.vars import structure_manager_list

class Tree(Blocks_manager):

	def __init__(self):
		Blocks_manager.__init__(self)

		self.block_id = 7
		self.blocks_parents = [
			(0,0)
		]
		self.durability = 15

	def generate_structure(self, position):
		structure = Structure(position)

		structure.add_block(5, (0,0))
		structure.add_block(5, (0,1))
		
		#leaves
		structure.add_block(6, (0,2))
		structure.add_block(6, (1,2))
		structure.add_block(6, (-1,2))
		structure.add_block(6, (2,2))
		structure.add_block(6, (-2,2))

		structure.add_block(6, (0,3))
		structure.add_block(6, (1,3))
		structure.add_block(6, (-1,3))
		structure_manager_list.append(structure)