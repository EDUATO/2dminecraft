from opensimplex import OpenSimplex



class Noise:
	def __init__(self, seed):
		self.seed = seed
		self.smoothness = 20
		self.tmp = OpenSimplex(seed=self.seed)

	def test(self, x, y, height):
		self.data = self.tmp.noise2d(x/self.smoothness, y) * height

		return round(self.data)