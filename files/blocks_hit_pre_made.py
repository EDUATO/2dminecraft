import pygame
from pygame.locals import *

import os

def unify_two_rects(rect1:pygame.Rect, rect2:pygame.Rect):
    output_rect = None
    max_height = 0
    leftest_point = 0
    # The tallest point
    if rect1.top > rect2.top: 
        max_height = rect1.top 
    else: 
        max_height = rect2.top

    # The leftest point
    if rect1.left < rect2.left: 
        leftest_point = rect1.left 
    else: 
        leftest_point = rect2.right
    
    #print(f"{rect1.right} / {rect2.left}")
    if (rect1.right == rect2.left):
        output_rect = pygame.Rect(leftest_point, rect1.y, rect1.width + rect2.width, rect1.height)

    """  if rect1.topright == rect2.topleft or rect1.topright == rect2.topleft:
        if rect1.bottom == rect2.top or rect2.bottom == rect1.top:
            """
    return output_rect

def unify_blocks_hitbox(rect_list:list)->list:
    """ The rect flow is from left to right and down to up """
    unions = [] # Rects unions hitboxes
    copied_rect_list = rect_list.copy()

    if len(copied_rect_list) != 0:
        rect_to_modify = copied_rect_list[0]
        rect_list.pop(0)

    for union in range(len(rect_list)):
        # Write down here
        if len(copied_rect_list) != 0: 
            rect_unified = unify_two_rects(rect_to_modify, copied_rect_list[0])
            if rect_unified != None: # If the modification was sucessful
                rect_to_modify = rect_unified
                copied_rect_list.remove(copied_rect_list[0])
            else:
                unions.append(rect_to_modify)
                rect_to_modify = copied_rect_list[0]
                copied_rect_list.pop(0)
        else: break # If copied_rect == 0

    return unions

                
