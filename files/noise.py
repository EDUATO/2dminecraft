from opensimplex import OpenSimplex

class Noise:
	def __init__(self, seed):
		self.seed = seed
		self.tmp = OpenSimplex(seed=seed)

	def test(self, x, y):
		self.data = self.tmp.noise2d(x, y)

		return self.data