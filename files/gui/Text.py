import pygame
from pygame.locals import *

from files.vars import modeX, modeY
import files.functions as f

class Text:
	def __init__(self, x, y, txt, FUENTE, COLOR, lock=None, screen_areas=(0, 0, modeX, modeY)):

		self.x = x
		self.y = y
		self.screen_areas = screen_areas
		
		self.Text = FUENTE.render(txt,1,(COLOR))

		self.w = self.Text.get_rect().width
		self.h = self.Text.get_rect().height
		self.Lock_formula = (0,0)

		self.change_lock(lock)

	def draw(self, surface):
		surface.blit(self.Text,(self.Lock_formula[0] + self.x,self.Lock_formula[1] + self.y))

	def change_lock(self, lock):
		self.set_lock_formula(lock)

	def set_lock_formula(self, lock):
		if not lock == None:
			self.Lock_formula = f.Lock_to(lock,0,0, width=self.w, height=self.h, screen_areas=self.screen_areas )

	def getHitbox(self):
		return pygame.Rect(self.Lock_formula[0] + self.x, self.Lock_formula[1] + self.y, self.w, self.h)

	def getWidth(self):
		return self.w

	def setCoords(self, x, y):
		self.x = x
		self.y = y