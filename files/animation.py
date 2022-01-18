

class animation:
	def __init__(self, limit, add):
		self.limit = limit
		self.add = add
	def classic_animation(self, limit, add, final_value):

		if limit > 0: # Positive
			if final_value < limit:
				return add
			else:
				return 0
		
		if limit < 0: # Negative
			if final_value > limit:
				return add
			else:
				return 0