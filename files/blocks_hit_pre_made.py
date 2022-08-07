import pygame
from pygame.locals import *

import os

def unify_two_rects(rect1:pygame.Rect, rect2:pygame.Rect, x_axis=True):
    
    output_rect = None
    leftest_point = 0
    
    # The leftest point
    if rect1.left < rect2.left: leftest_point = rect1.left 
    else: leftest_point = rect2.right

    if (rect1.right == rect2.left) and (rect1.y == rect2.y):
        output_rect = pygame.Rect(leftest_point, rect2.y, rect1.width + rect2.width, rect2.height)



    #if rect1.right == rect2.left or rect1.right == rect2.left:

    return output_rect

def unify_blocks_hitbox(rect_list:list, x_axis=True)->list:
    """Must be sorted from left to right and down to up """
    unions = [] # Rects unions hitboxes
    copied_rect_list = rect_list.copy()

    rect_to_modify = copied_rect_list[0]
    copied_rect_list.pop(0)

    for union in range(len(rect_list)):
        # Write down here
        if len(copied_rect_list) != 0: 
            rect_unified = unify_two_rects(rect_to_modify, copied_rect_list[0], x_axis=x_axis)
            if rect_unified != None: # If the modification was sucessful
                rect_to_modify = rect_unified
            else:
                unions.append(rect_to_modify)
                rect_to_modify = copied_rect_list[0]
            copied_rect_list.pop(0)
        else: 
            unions.append(rect_to_modify)
            break # If copied_rect == 0

    return unions

def unify_algorithm(rect_list:list):
    output = unify_blocks_hitbox(rect_list)
    return output

                
