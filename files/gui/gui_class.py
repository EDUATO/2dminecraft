import pygame

from files.blocks.every_block_data import get_every_block_list
from files.vars import modeY, modeX, gui_scale
import files.functions as f
from files.gui.Text import Text

inGui = (False, False) # This will control if the user is in any type of GUI
class Gui:
	def __init__(self, App, sprite):
		Blocks_texture = App.assets.Blocks_texture
		self.blocks_texture = pygame.transform.scale(Blocks_texture, (Blocks_texture.get_width() * gui_scale, Blocks_texture.get_height() * gui_scale))
		self.sprite = sprite
		self.picked_item = [None, 0] # The item ID and the amount
		self.pressed = [False, False] # Right click and Left click
		self.prew_slot_id = 0
		self.used_slots_id = []
		

	def setInGui(self, state, gui_type_class):
		global inGui
		inGui = (state, gui_type_class)

	def slots_update(self, App, slots):

		self.mouse_action = pygame.mouse.get_pressed()

		for i in range(len(slots)):
			self.Slot_Rect_Tuple = (
									((slots[i]["Pos"][0] * gui_scale) + modeX/2 - self.sprite.get_width()/2), # X
								 	((slots[i]["Pos"][1] * gui_scale) + modeY/2 - self.sprite.get_height()/2), # Y
								 	(slots[i]["Pos"][2] * gui_scale) , # Width
								 	(slots[i]["Pos"][3] * gui_scale) # Height
								)
			
			self.Slot_Rect = pygame.Rect( self.Slot_Rect_Tuple )

			# Draw whats inside the slot
			if not slots[i]["Item"][0] == None:
				drawInventoryItem(App, self.blocks_texture, slots[i]["Item"], self.Slot_Rect_Tuple[0], self.Slot_Rect_Tuple[1])

			self.slots_action(App=App ,slots=slots, slot_num=i)

	def slots_action(self, App, slots, slot_num):
		# Mouse colliderect
			if App.mouse_hitbox.colliderect(self.Slot_Rect):
				if not slot_num == self.prew_slot_id:
					self.pressed[0] = False # Right Click
					self.pressed[1] = False	# Left Click
					self.prew_slot_id = slot_num
					
				# Draw Slot Selection Shadow
				self.SlotSelection(App.surface)
				
				self.__LeftClickController__(slots, slot_num)

				self.__RightClickController__( slots, slot_num)

			self.itemInCursor(App, self.picked_item)

	def SlotSelection(self, surface):
		self.Slot_RectSurface = pygame.Surface( (self.Slot_Rect[2], self.Slot_Rect[3]), pygame.SRCALPHA )
		self.Slot_RectSurface.fill((255,255,255,150))
		surface.blit(self.Slot_RectSurface, (self.Slot_Rect[0], self.Slot_Rect[1]))

	def __LeftClickController__(self, slots, slot_num):
		""" Control the GUI Left Click Events """

		# If only the Left click is pressed
		if self.mouse_action[0] == 1 and self.pressed[0] == False:
			self.pressed[0] = True

			if self.picked_item[0] == None:
				# Grab one item if the mouse has no item
				self.picked_item = [slots[slot_num]["Item"][0], slots[slot_num]["Item"][1]]
				self.replace_slot(slots=slots, item=[None, 0], slot_id=slot_num)

			elif self.picked_item[0] != None:
				# Leave the item in the Inventory
				if slots[slot_num]["Item"][0] == None:
					self.replace_slot(slots=slots, item=self.picked_item, slot_id=slot_num)
					self.picked_item = [None, 0]

				# Convine the item with another with the same id
				elif slots[slot_num]["Item"][0] == self.picked_item[0]:
					self.replace_slot(slots=slots, item=self.picked_item, slot_id=slot_num, add=self.picked_item[1])
					self.picked_item = [None, 0]

				# Switch places with the inventory item with the picked one
				elif slots[slot_num]["Item"][0] != self.picked_item[0]:
					a = list(slots[slot_num]["Item"])
					self.replace_slot(slots=slots, item=self.picked_item, slot_id=slot_num)
					self.picked_item = a
					
					
					
		# Reset pressed[0] to False
		elif self.mouse_action[0] == 0 and self.pressed[0] == True:
			self.pressed[0] = False

	def __RightClickController__(self, slots, slot_num):
		""" Control the GUI Right Click Events """

		# If only the right click is pressed
		if self.mouse_action[2] == 1 and self.pressed[1] == False:
			self.pressed[1] = True

			if self.picked_item[0] == None and not slots[slot_num]["Item"][0] == None:
				# Grab half the item amount
				if slots[slot_num]["Item"][1] > 1:
					self.calc = slots[slot_num]["Item"][1]//2
					self.picked_item = [slots[slot_num]["Item"][0], slots[slot_num]["Item"][1] - self.calc]
					slots[slot_num]["Item"][1] = self.calc

			# Leave one Item in the slot
			elif self.picked_item[0] != None:
				# Add one item
				if self.picked_item[0] != slots[slot_num]["Item"][0] or slots[slot_num]["Item"][0] == None:
					if not slot_num in self.used_slots_id:
						# Leave an item in a slot with the same id
						if not slots[slot_num]["Item"][0] == None:
							if not self.picked_item[0] == None:
								slots[slot_num]["Item"][1] += 1

							if self.picked_item[1] >= 1:
								self.picked_item[1] -= 1
										
						else: # Leave an item in an empty slot
							# Allows the "dragged" movement
							slots[slot_num]["Item"] = [self.picked_item[0], 1]
							self.picked_item[1] -= 1


						if self.picked_item[1] <= 0:
							self.picked_item =  [None, 0]

						# Will keep a list with all the used slots when dragged movement is made
						self.used_slots_id.append(slot_num)

		# Reset pressed[1] and used_slots_id
		elif self.mouse_action[2] == 0 and self.pressed[1] == True:
			self.pressed[1] = False	
			self.used_slots_id = []

	def replace_slot(self,slots, item, slot_id, add=False):
		slots[slot_id]["Item"][0] = item[0]
		
		if add == 0:
			slots[slot_id]["Item"][1] = item[1]

		elif add != False:
			slots[slot_id]["Item"][1] += add

	def itemInCursor(self, App, item_id):
		mouse_pos = pygame.mouse.get_pos()
		drawInventoryItem(App,self.blocks_texture, item_id,X=mouse_pos[0], Y=mouse_pos[1], centered=True)

def drawInventoryItem(App, blocks_texture, item_id, X=0, Y=0, centered=False):
	every_block_list = get_every_block_list(App)
	if item_id[0] != None:
		try:
			crop = (
										every_block_list[item_id[0]]["crop"][0] * gui_scale,
			 							every_block_list[item_id[0]]["crop"][1] * gui_scale, 
										every_block_list[item_id[0]]["crop"][2] * gui_scale,
					 					every_block_list[item_id[0]]["crop"][3] * gui_scale
									)

		except Exception as e:
			print(f"There is no block with the id {item_id[0]} - Error {e}")
			return False # There is no block 

		color = (250,250,250)

		if item_id [1] != 1:
			ItemText = Text(x=X , y=Y, txt=str(item_id[1]),FUENTE=App.assets.Mc_20, COLOR=color, lock=None, screen_areas=(X - 16, Y - 16, gui_scale, gui_scale))
		# Draw Text
		if centered:
			App.surface.blit(blocks_texture, (X - (16 * gui_scale)/2 , Y - (16 * gui_scale)/2), crop)
			if item_id [1] != 1:
				ItemText.setCoords(	x= X - (16 * gui_scale)/2,
									y= Y - (16 * gui_scale)/2
				)
				
				ItemText.draw(App)

		else:
			App.surface.blit(blocks_texture, (X , Y), crop)
			if item_id [1] != 1:
				ItemText.draw(App)

		
		