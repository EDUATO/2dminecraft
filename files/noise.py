from opensimplex import OpenSimplex



class Noise:
	def __init__(self, seed):
		self.seed = seed
		self.smoothness = 25
		self.tmp = OpenSimplex()

	def test(self, x, y, height):
		print(height)
		self.data = self.tmp.noise2d(x/self.smoothness, y) * height

		return self.data