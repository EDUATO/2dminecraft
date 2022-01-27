from opensimplex import OpenSimplex



class Noise:
	def __init__(self, seed):
		self.seed = seed
		self.smoothness = 10
		self.tmp = OpenSimplex()

	def test(self, x, y, height):
		self.data = self.tmp.noise2d(x/self.smoothness, y*100) * height/3

		return self.data