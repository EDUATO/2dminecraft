from files.blocks.blocks_man import Blocks_manager
from files.terrain.structure import Structure
from files.vars import structure_manager_list

class Tree(Blocks_manager):

	def __init__(self, App):
		Blocks_manager.__init__(self, App)

		self.block_id = 7
		self.blocks_parents = [
			(0,0)
		]
		self.durability = 15

	def generate_structure(self, position):
		structure = Structure(position)

		# Dirt block
		structure.add_block(3, (0,0))

		structure.add_block(5, (0,1))
		structure.add_block(5, (0,2))
		
		#leaves
		structure.add_block(6, (0,3))
		structure.add_block(6, (1,3))
		structure.add_block(6, (-1,3))
		structure.add_block(6, (2,3))
		structure.add_block(6, (-2,3))

		structure.add_block(6, (0,4))
		structure.add_block(6, (1,4))
		structure.add_block(6, (-1,4))
		structure_manager_list.append(structure)