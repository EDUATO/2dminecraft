import pygame
from pygame.locals import *

from files.gui.gui_class import Gui, inGui
from files.vars import win, modeX, modeY, block_scale_buff, slot_size
from files.import_imp import Inventory_texture, Blocks_texture
import files.bucle as b
import files.Game as gm

inInventory = False

Inventory_slots = {}

def setInventorySlots():
	global Inventory_slots
	a = 0

	# Hotbar slots
	for x in range(9):
		Inventory_slots[a] = {"Item" : [a+1, 64], "Pos":(8 + ( (2 + slot_size) * x), 140 + 2 , slot_size, slot_size)}
		a += 1

	# Inventory slots
	for y in range(3):
		for x in range(9):
			Inventory_slots[a] = {"Item" : [None, None], "Pos":(8 + ( (2 + slot_size) * x), 84 + ( (2 + slot_size) * y), slot_size, slot_size)}
			a += 1

	# Armor slots

	for y in range(4):
		Inventory_slots[a] = {"Item" : [None, None], "Pos":(6 + (2),8 + ( (2 + slot_size) * y), slot_size, slot_size)}
		a += 1

	# Second hand
	Inventory_slots[a] = {"Item" : [None, None], "Pos":(76 + 1, 61 + 1 , slot_size, slot_size)}
	a += 1

	# Crafting
	for y in range(2):
		for x in range(2):
			Inventory_slots[a] = {"Item" : [None, None], "Pos":(98 + ( (2 + slot_size) * x), 18 + ( (2 + slot_size) * y), slot_size, slot_size)}
			a += 1

	# Crafting result
	Inventory_slots[a] = {"Item" : [None, None], "Pos":(153 + (1), 27 + (1), slot_size, slot_size)}
	a += 1

setInventorySlots()



class Inventory(Gui):
	def __init__(self):
		self.transformed_sprite = pygame.transform.scale(Inventory_texture, (Inventory_texture.get_width() * block_scale_buff,  Inventory_texture.get_height() * block_scale_buff))
		super().__init__(self.transformed_sprite)

	def open(self):
		global inInventory
		self.setInGui(True)
		inInventory = True
		pygame.mouse.set_visible(True)

	def close(self):
		global inInventory
		self.setInGui(False)
		inInventory = False
		pygame.mouse.set_visible(False)

	def update(self, mouse, keys):
		if inInventory == True:
			win.blit(self.sprite, (modeX/2 - self.sprite.get_width()/2 , modeY/2 - self.sprite.get_height()/2))

			self.slots_update(slots=Inventory_slots, mouse=mouse)

		if not gm.Pause:
			self.key_update(keys)

	def key_update(self, keys):
		if keys[K_ESCAPE] == 1:
			self.close()

		elif keys[K_e] == 1:
			self.open()


PlayerInventory = Inventory()