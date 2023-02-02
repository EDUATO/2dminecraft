import pygame

from files.gui.gui_class import inGui

def player_mouse_cotroller(chunks_list, mouse_hitbox, entity_classes):
	selected_block = None
	mouse_touching_entity = False
	#print(inGui)
	for c in range(len(chunks_list)):
		for i in range(len(chunks_list[c].blocks)):
			# Detect a block being touched by the cursor
			mouse_col_block = chunks_list[c].blocks[i].coll_hitbox2(mouse_hitbox)

			if mouse_col_block and not inGui[0]:
				selected_block = chunks_list[c].blocks[i]

				block_rect = selected_block.getHitbox()

				# DETECT IF THE BLOCK THAT THE MOUSE IS TOUCHING IS COLLIDERECTING AN ENTITY
				for i in range(len(entity_classes)):
					if block_rect.colliderect(pygame.Rect(entity_classes[i].get_hitbox())):
						mouse_touching_entity = True
						break

				if mouse_touching_entity:
					selected_block.setglow(True, color=(200, 0, 0))
				else:
					selected_block.setglow(True, color=(255,255,0))
				
			else:
				chunks_list[c].blocks[i].resetBreakState() # Reset break state
				chunks_list[c].blocks[i].setglow(False)

	return selected_block, mouse_touching_entity