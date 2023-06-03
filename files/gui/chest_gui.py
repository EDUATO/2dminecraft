import pygame
from pygame.locals import *

from files.gui.gui_class import Gui
from files.vars import modeX, modeY, slot_size, gui_scale
from files.blocks.every_block_data import get_every_block_list
import files.Game as gm

class ChestContainer(Gui):
	def __init__(self, App):
		self.transformed_sprite = App.assets.Chest_con_texture
		self.Inventory_slots = {}
		self.In_Inventory = False
		self.Pause = False
		self.setInventorySlots()
		self.add_item(inventory_slot=20, item_id=4, amount=64)

		super().__init__(App, self.transformed_sprite)

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

		# Chest slots
		for z in range(3):
			for x in range(9):
				self.Inventory_slots[a] = {"Item" : [None, None], "Pos":(8 + ( (2 + slot_size) * x), 18 + ( (2 + slot_size) * z), slot_size, slot_size)}
				a += 1

	def open(self):
		self.setInGui(True, self)
		self.In_Inventory = True
		pygame.mouse.set_visible(True)

	def close(self):
		self.setInGui(False, False)
		self.In_Inventory = False
		pygame.mouse.set_visible(False)

	def update(self, App, keys):
		if self.In_Inventory == True:
			App.surface.blit(self.sprite, (modeX/2 - self.sprite.get_width()/2 , modeY/2 - self.sprite.get_height()/2))

			self.slots_update(App,slots=self.Inventory_slots)

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
