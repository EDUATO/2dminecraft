import pygame
from pygame.locals import *

from files.gui.Inventory import Inventory_slots
from files.import_imp import Widgets_texture
from files.vars import win, modeX, modeY, block_scale_buff
from files.fonts import *
import files.functions as f
from files.Block import Blocks_list, block_texture

class Hotbar:
	def __init__(self):
		self.texture = pygame.transform.scale(Widgets_texture, (Widgets_texture.get_width() * block_scale_buff, Widgets_texture.get_height() * block_scale_buff))
		self.bar_crop = (0,0,182 * block_scale_buff,22 * block_scale_buff)
		self.bar_selector_crop = (0, 22 * block_scale_buff, 24 * block_scale_buff, 24 * block_scale_buff)
		self.slot_pos = 0
		self.slot_size = 20
		self.slots = []

	def update(self, events):

		# Get slots from Inventory
		self.slots = []
		for i in range(9):
			self.slots.append(Inventory_slots[i])

		win.blit(self.texture , (modeX/2 - self.texture.get_width()/2,modeY - self.bar_crop[3] - 20), self.bar_crop)
		#pygame.draw.rect(win, (255,255,0), pygame.Rect(modeX/2 - self.texture.get_width()/2,modeY - self.bar_crop[3] - 20, self.bar_crop[2], self.bar_crop[3]), 2)

		self.mouse_wheel(events)

		self.show_items()

		win.blit(self.texture, ((modeX/2 - self.texture.get_width()/2 - 3) + ((self.slot_pos ) * (self.slot_size * block_scale_buff)) ,modeY - self.bar_crop[3] - 23), self.bar_selector_crop)

	def show_items(self):
		for i in range(len(self.slots)):
			if not self.slots[i]["Item"][0] == None:
				try:
					self.crop = (Blocks_list[self.slots[i]["Item"][0]]["crop"][0] * block_scale_buff, Blocks_list[self.slots[i]["Item"][0]]["crop"][1] * block_scale_buff, 
					Blocks_list[self.slots[i]["Item"][0]]["crop"][2] * block_scale_buff, Blocks_list[self.slots[i]["Item"][0]]["crop"][3] * block_scale_buff)
				except:
					self.slots[i]["Item"] = [None, None]
					self.crop = (0,0,0,0)

				win.blit(block_texture, ((modeX/2 - self.texture.get_width()/2) + 9 + (i) * (self.slot_size * block_scale_buff), modeY - self.bar_crop[3] - 11), self.crop)

				if not self.slots[i]["Item"][1] == 1:
					f.text(str(self.slots[i]["Item"][1]), (modeX/2 - self.texture.get_width()/2 + 10) + (i ) * (self.slot_size * block_scale_buff), modeY - self.bar_crop[3] - 10, Arial_30, (255,255,0) )

	def mouse_wheel(self, events):
		for event in events:
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 5:
					if self.slot_pos < 8:
						self.slot_pos += 1
					else:
						self.slot_pos = 0

				elif event.button == 4:
					if self.slot_pos > 0:
						self.slot_pos -= 1
					else:
						self.slot_pos = 8

	def keys(self, keys):
		pass

	def get_slot_item(self):
		try:
			return self.slots[self.slot_pos]
		except:
			return None
		