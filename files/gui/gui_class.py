import pygame

from files.Block import Blocks_list, block_texture
from files.vars import modeY, modeX, win, block_scale_buff
import files.functions as f
from files.fonts import *

inGui = False

class Gui:
	def __init__(self, sprite):
		self.sprite = sprite
		self.picked_item = [None, 0]
		self.pressed = [False, False]
		self.prew_slot_id = 0
		self.block_focused_id = 0

	def setInGui(self, state):
		global inGui
		inGui = state

	def update(self):
		pass

	def Slots_update(self, slots, mouse):

		self.mouse_action = pygame.mouse.get_pressed()

		for i in range(len(slots)):
			self.Slot_Rect = pygame.Rect( (slots[i]["Pos"][0] * block_scale_buff) + modeX/2 - self.sprite.get_width()/2, (slots[i]["Pos"][1] * block_scale_buff) + modeY/2 - self.sprite.get_height()/2, slots[i]["Pos"][2] * block_scale_buff,slots[i]["Pos"][3] * block_scale_buff)

			#pygame.draw.rect(win, (255,255,0), self.Slot_Rect, 2)

			# Draw whats inside the slot
			if not slots[i]["Item"][0] == None:
				self.crop = (Blocks_list[slots[i]["Item"][0]]["crop"][0] * block_scale_buff, Blocks_list[slots[i]["Item"][0]]["crop"][1] * block_scale_buff, 
				Blocks_list[slots[i]["Item"][0]]["crop"][2] * block_scale_buff, Blocks_list[slots[i]["Item"][0]]["crop"][3] * block_scale_buff)

				win.blit(block_texture, (self.Slot_Rect[0], self.Slot_Rect[1]), self.crop )

				if not slots[i]["Item"][1] == 1:
					f.text(str(slots[i]["Item"][1]), self.Slot_Rect[0] + self.Slot_Rect[2] - 40, self.Slot_Rect[1] + self.Slot_Rect[3] - 40, Arial_30, (255,255,0) )

			# Mouse colliderect
			if mouse.colliderect(self.Slot_Rect):
				if not i == self.prew_slot_id:
					self.pressed[1] = False	
					self.pressed[0] = False
					self.prew_slot_id = i


				self.Slot_RectSurface = pygame.Surface( (self.Slot_Rect[2], self.Slot_Rect[3]), pygame.SRCALPHA )
				self.Slot_RectSurface.fill((255,255,255,150))
				win.blit(self.Slot_RectSurface, (self.Slot_Rect[0], self.Slot_Rect[1]))
				
				# Left click
				if self.mouse_action[0] == 1 and self.pressed[0] == False:
					self.pressed[0] = True
					if self.picked_item[0] == None:
						self.picked_item = [slots[i]["Item"][0], slots[i]["Item"][1]]
						self.replace_slot(slots=slots, item=[None, 0], slot_id=i)

					elif self.picked_item[0] != None:
						if slots[i]["Item"][0] == None:
							self.replace_slot(slots=slots, item=self.picked_item, slot_id=i)
							self.picked_item = [None, 0]

						elif slots[i]["Item"][0] == self.picked_item[0]:
							self.replace_slot(slots=slots, item=self.picked_item, slot_id=i, add=self.picked_item[1])
							self.picked_item = [None, 0]
							

				elif self.mouse_action[0] == 0 and self.pressed[0] == True:
					self.pressed[0] = False


				# Right click
				if self.mouse_action[2] == 1 and self.pressed[1] == False:
					self.pressed[1] = True

					if self.picked_item[0] == None:
						# Divide the items amount
						if slots[i]["Item"][1] > 1:
							self.calc = slots[i]["Item"][1]//2

							self.picked_item = [slots[i]["Item"][0], slots[i]["Item"][1] - self.calc]

							slots[i]["Item"][1] = self.calc

					elif self.picked_item[0] != None:
						# Add one item
						if self.picked_item[0] == slots[i]["Item"][0] or slots[i]["Item"][0] == None:
							if not slots[i]["Item"][0] == None:
								if not self.picked_item[0] == None:
									slots[i]["Item"][1] += 1

								if self.picked_item[1] >= 1:
									self.picked_item[1] -= 1
											
							else:
								slots[i]["Item"] = [self.picked_item[0], 1]
								self.picked_item[1] -= 1

							if self.picked_item[1] <= 0:
								self.picked_item =  [None, 0]


				elif self.mouse_action[2] == 0 and self.pressed[1] == True:
					self.pressed[1] = False	

			self.itemInCursor(mouse, self.picked_item)

	def replace_slot(self,slots, item, slot_id, add=False):
		slots[slot_id]["Item"][0] = item[0]
		
		if add == 0:
			slots[slot_id]["Item"][1] = item[1]

		elif add != False:
			slots[slot_id]["Item"][1] += add

	def itemInCursor(self, mouse, item_id):
		if not item_id[0] == None:
			try:
				self.crop = (Blocks_list[item_id[0]]["crop"][0] * block_scale_buff, Blocks_list[item_id[0]]["crop"][1] * block_scale_buff, 
						Blocks_list[item_id[0]]["crop"][2] * block_scale_buff, Blocks_list[item_id[0]]["crop"][3] * block_scale_buff)

			except:
				self.crop = (0,0,0,0)

			win.blit(block_texture, (mouse[0] - 16 * block_scale_buff/2 , mouse[1] - 16 * block_scale_buff/2), self.crop)
		