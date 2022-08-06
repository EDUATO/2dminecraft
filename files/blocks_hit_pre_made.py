import pygame
from pygame.locals import *

def unify_two_rects(rect1:pygame.Rect, rect2:pygame.Rect):
    output_rect = None
    if rect1.bottom == rect2.top:
        output_rect = rect1.union(rect2)

    """  if rect1.topright == rect2.topleft or rect1.topright == rect2.topleft:
        if rect1.bottom == rect2.top or rect2.bottom == rect1.top:
            """
    return output_rect

def unify_blocks_hitbox(rect_list:dict)->list:
    unions = [] # Rects unions hitboxes
    copied_rect_list = rect_list.copy()
    for union in range(len(rect_list)):
        new_union_list = None
        len_copied_rect_list = len(copied_rect_list)
        for i in range(len_copied_rect_list):
            try:
                if new_union_list != None:
                    # Unify two rects
                    unified = unify_two_rects(new_union_list, copied_rect_list[i])
                    if unified != None:
                        new_union_list = unified
                        copied_rect_list.pop(i)
                    else: break
                else: 
                    new_union_list = copied_rect_list[i]
                    copied_rect_list.pop(i)

            except IndexError:
                        break

        unions.append(new_union_list)

        if len(copied_rect_list) == 0:break

    return unions

                
