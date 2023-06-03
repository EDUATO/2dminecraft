from files.blocks.blocks_man import Blocks_manager
from files.terrain.structure import Structure
from files.vars import structure_manager_list

class House(Blocks_manager):

	def __init__(self, App):
		Blocks_manager.__init__(self, App)

		self.block_id = 8
		self.blocks_parents = [
			(0,0)
		]
		self.durability = 1

	def generate_structure(self, position):
		structure = Structure(position)

		# Wooden Planks floor
		for i in range(10):
			structure.add_block(9, (i,0))

		# Wooden walls
		for i in range(4):
			structure.add_block(5, (9,i+1))
		for i in range(4):
			structure.add_block(5, (0,i+1))

		# Roof
		for i in range(12):
			structure.add_block(9, (i-1,5))

		structure_manager_list.append(structure)
		