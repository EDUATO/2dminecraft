from opensimplex import OpenSimplex



class Noise:
	def __init__(self, seed):
		self.seed = seed
		self.smoothness = 30
		self.tmp = OpenSimplex()

	def test(self, x, y, height):
		self.data = self.tmp.noise2d(x/self.smoothness, y*100) * height/2

		return self.data