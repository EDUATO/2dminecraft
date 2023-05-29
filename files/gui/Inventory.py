import pygame
from pygame.locals import *

from files.gui.gui_class import Gui
from files.vars import modeX, modeY, slot_size, gui_scale
from files.blocks.every_block_data import every_block_list
from files.import_imp import Inventory_texture
import files.mainLoop as b
import files.Game as gm

class Inventory(Gui):
	def __init__(self):
		self.transformed_sprite = pygame.transform.scale(Inventory_texture, (Inventory_texture.get_width() * gui_scale,  Inventory_texture.get_height() * gui_scale))
		self.Inventory_slots = {}
		self.In_Inventory = False
		self.Pause = False
		self.setInventorySlots()
		# Append every item
		for i in range(len(every_block_list) - 1): # To ignore air_block
			self.add_item(inventory_slot=i, item_id=i+1, amount=64)

		super().__init__(self.transformed_sprite)

	def setInventorySlots(self):
		a = 0

		# Hotbar slots
		for x in range(9):
			self.Inventory_slots[a] = {"Item" : [None, None], "Pos":(8 + ( (2 + slot_size) * x), 140 + 2 , slot_size, slot_size)}
			a += 1

		# Inventory slots
		for y in range(3):
			for x in range(9):
				self.Inventory_slots[a] = {"Item" : [None, None], "Pos":(8 + ( (2 + slot_size) * x), 84 + ( (2 + slot_size) * y), slot_size, slot_size)}
				a += 1

		# Armor slots
		for y in range(4):
			self.Inventory_slots[a] = {"Item" : [None, None], "Pos":(6 + (2),8 + ( (2 + slot_size) * y), slot_size, slot_size)}
			a += 1

		# Second hand
		self.Inventory_slots[a] = {"Item" : [None, None], "Pos":(76 + 1, 61 + 1 , slot_size, slot_size)}
		a += 1

		# Crafting
		for y in range(2):
			for x in range(2):
				self.Inventory_slots[a] = {"Item" : [None, None], "Pos":(98 + ( (2 + slot_size) * x), 18 + ( (2 + slot_size) * y), slot_size, slot_size)}
				a += 1

		# Crafting result
		self.Inventory_slots[a] = {"Item" : [None, None], "Pos":(153 + (1), 27 + (1), slot_size, slot_size)}
		a += 1

	def open(self):
		self.setInGui(True, self)
		self.In_Inventory = True
		pygame.mouse.set_visible(True)

	def close(self):
		self.setInGui(False, False)
		self.In_Inventory = False
		pygame.mouse.set_visible(False)

	def update(self, surface, mouse, keys):
		if self.In_Inventory == True:
			surface.blit(self.sprite, (modeX/2 - self.sprite.get_width()/2 , modeY/2 - self.sprite.get_height()/2))

			self.slots_update(surface,slots=self.Inventory_slots, mouse=mouse)

		if self.Pause == False:
			self.__key_update(keys)

	def getInventorySlots(self):
		return self.Inventory_slots

	def __key_update(self, keys):
		if keys[K_ESCAPE] == 1:
			self.close()

		elif keys[K_e] == 1:
			self.open()

	def add_item(self, inventory_slot:int, item_id, amount):
		if self.Inventory_slots[inventory_slot]["Item"][0] == item_id:
			self.Inventory_slots[inventory_slot]["Item"][0] = item_id
			self.Inventory_slots[inventory_slot]["Item"][1] = abs(amount - self.Inventory_slots["Item"][1])

		if self.Inventory_slots[inventory_slot]["Item"][0] == None:
			self.Inventory_slots[inventory_slot]["Item"][0] = item_id
			self.Inventory_slots[inventory_slot]["Item"][1] = amount
