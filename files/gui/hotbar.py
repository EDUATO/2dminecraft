import pygame
from pygame.locals import *

from files.import_imp import Widgets_texture
from files.vars import modeX, modeY, block_scale_buff
from files.fonts import *
import files.functions as f
import files.mainLoop as b
import files.Game as gm
from files.gui.Text import Text
from files.gui.gui_class import drawInventoryItem
from files.blocks.block_data import every_block_list

class Hotbar:
	def __init__(self):
		self.texture = pygame.transform.scale(Widgets_texture, (Widgets_texture.get_width() * block_scale_buff, Widgets_texture.get_height() * block_scale_buff))
		self.bar_crop = (0,0,182 * block_scale_buff,22 * block_scale_buff)
		self.bar_selector_crop = (0, 22 * block_scale_buff, 24 * block_scale_buff, 24 * block_scale_buff)
		self.slot_pos = 0
		self.slot_size = 20
		self.Pause = False
		self.slots = []

	def update(self, events, surface, Inventory_slots):

		# Update the slots from Inventory
		self.slots = []
		for i in range(9):
			self.slots.append(Inventory_slots[i])
		
		# Draw HotBar
		surface.blit(self.texture , (modeX/2 - self.texture.get_width()/2,modeY - self.bar_crop[3] - 20), self.bar_crop)

		if self.Pause == False:
			self.mouse_wheel(events)

		self.show_items(surface)
		
		# Draw HotBar Selector
		surface.blit(self.texture, ((modeX/2 - self.texture.get_width()/2 - 3) + ((self.slot_pos ) * (self.slot_size * block_scale_buff)) ,modeY - self.bar_crop[3] - 23), self.bar_selector_crop)

	def show_items(self, surface):
		# Draw the player's items
		for i in range(len(self.slots)):
			if not self.slots[i]["Item"][0] == None:
				DR = drawInventoryItem(surface=surface,
									item_id= self.slots[i]["Item"],
									X= (modeX/2 - self.texture.get_width()/2 + 9) + (i) * (self.slot_size * block_scale_buff), 
									Y= (modeY - self.bar_crop[3] - 11) )
				if self.slots[i] == self.get_slot_item():
					Text(0, modeY - self.bar_crop[3] - 50, every_block_list[self.slots[i]["Item"][0]]["Name"], Mc_15, (235,235,235), lock="x").draw(surface)

				if DR == False:
					self.slots[i]["Item"] = [None, None]
				

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
		