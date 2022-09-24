from files.functions import detect_chunk_with_position

class Structure:
	def __init__(self, center_grid_position:tuple):
		# Where the structure will spawn
		self.center_grid_position = center_grid_position
		self.center_pos_chunk = detect_chunk_with_position(self.center_grid_position)

		self.blocks_list = []

	def add_block(self, id:int, position:tuple):
		""" Position acording to the structure center """
		self.blocks_list.append(
			{"id":id,
			"pos":(self.center_grid_position[0] + position[0], self.center_grid_position[1] + position[1])}
		)