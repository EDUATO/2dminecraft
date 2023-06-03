import pygame
from pygame.locals import *

from files.vars import block_scale_buff

class Physics:
    def __init__(self,
        hitbox_size
    ):
        self.gravity = 9.8

        self.vel_y = 0

        self.hitbox_size = hitbox_size

        self.dx = 0
        self.return_dx = 0
        
        self.reload_diferences()

    def reload_diferences(self):
        # X and Y diferences
        self.return_dx = 0
        self.dy = 0

        #Player's hitbox collition
        self.entity_collition_type = {
            "right":False,"right-block":None,  # right: Where the collition came from. "right-block": The nearest right-block
            "left":False, "left-block":None,
            "bottom":False, "bottom-block":None,
            "top":False, "top-block":None
        } 

    def update(self, chunks_list, surface, screen_pos, deltaTime=1):
        self.reload_diferences()
        # Gravity
        self.vel_y = self.update_gravity(self.vel_y) 
        self.dy += round(self.vel_y*deltaTime)


        self.screen_entity_hitbox = (screen_pos[0], screen_pos[1], self.hitbox_size[0], self.hitbox_size[1])

        # Get blocks near the entity
        collided_blocks = self.nearbyblocks(chunks_list, self.screen_entity_hitbox)


        # X PHYSICS
        self.x_physics(collided_blocks, surface, screen_pos)
        

        # Y PHYSICS
        self.y_physics(collided_blocks, surface, screen_pos)
        

        # Detect collition in two places at the same time
        collitions_detected:int = 0
        if self.entity_collition_type["right"]: 
            collitions_detected += 1
        if self.entity_collition_type["left"]: 
            collitions_detected += 1
        if self.entity_collition_type["bottom"]: 
            collitions_detected += 1
        if self.entity_collition_type["top"]: 
            collitions_detected += 1
            
        if collitions_detected < 2:
            self.applyX_physics_changes()
        self.applyY_physics_changes()
        
        #self.dx = 0
    def update_gravity(self, vel_y:int, deltaTime=1):
        vel_y += deltaTime
        if vel_y > self.gravity:
            vel_y = self.gravity
        return vel_y

    def nearbyblocks(self, chunks_list, hitbox:tuple):
        """ Between all the blocks from the screen detect the ones that are closer to the player """
        increaseSize = 200
        biggerHitbox = [ # Make the entity hitbox bigger to detect the surrounding blocks
                    hitbox[0] - increaseSize//2,
                    hitbox[1] - increaseSize//2,
                    hitbox[2] + increaseSize,
                    hitbox[3] + increaseSize
        ]
        # dx and dy comprobations
        if self.dx >= 0:
            biggerHitbox[2] += self.dx
        elif self.dx < 0: # Remember self.dx is NEGATIVE
            biggerHitbox[0] += self.dx
            biggerHitbox[2] -= self.dx

        if self.dy >= 0:
            biggerHitbox[3] += self.dy
        elif self.dy < 0: # Remember self.dy is NEGATIVE
            biggerHitbox[1] += self.dy
            biggerHitbox[3] -= self.dy

        
        output = []
        for c in range(len(chunks_list)): # Active chunks
            for i in range(len(chunks_list[c].blocks)): # Blocks from each chunk
                if chunks_list[c].blocks[i].coll_hitbox2(pygame.Rect(biggerHitbox)):
                    output.append(chunks_list[c].blocks[i])
                    chunks_list[c].blocks[i].setglow(True)
        
        return output

    def get_nearest_block(
        self,
        direction, # left - right - up - bottom
        collided_blocks
        ):
        nearest_block = None
        index = 0

        if direction == "left" or direction == "right":
            index = 0 # x coords
        elif direction == "up" or direction == "bottom":
            index = 1 # y coords
        for j in range(len(collided_blocks)):
            block = collided_blocks[j] # Blocks that the entity collided

            grid_pos = block.getGridCoords()[index]

            if nearest_block != None:
                if direction == "left" or direction == "up":
                    if grid_pos <= nearest_block.getGridCoords()[index]:
                        nearest_block = block
                elif direction == "right" or direction == "bottom":
                    if grid_pos >= nearest_block.getGridCoords()[index]:
                        nearest_block = block

                nearest_block.setglow(True, color=(200,0,0))
            else: # nearest_block IS None
                nearest_block = block

        return nearest_block

    def collided_block_tiles(self, blocks_list, rect_formula, ignore=[]):
        blocks_pos = []

        collided_blocks = []
        for i in range(len(blocks_list)):
            blocks_pos.append(blocks_list[i].getGridCoords())
            #blocks_list[i].setglow(True)
            if blocks_list[i].coll_hitbox(Rect=pygame.Rect(rect_formula), undetectable_ids=[0]):
                collided_blocks.append(blocks_list[i])
                    

        return collided_blocks

    def x_physics(self, every_block_list, surface, screen_pos):
        # Check X collition
        if self.dx >= 0:
            x_rect_formula = (screen_pos[0], screen_pos[1] , self.hitbox_size[0] + self.dx, self.hitbox_size[1])
        elif self.dx < 0: # Will add the NEGATIVE self.dx to screen_pos
            x_rect_formula = (screen_pos[0] + self.dx, screen_pos[1] , self.hitbox_size[0] - self.dx, self.hitbox_size[1])

        x_collided = self.collided_block_tiles(blocks_list=every_block_list, 
                                                    rect_formula=x_rect_formula)

        #pygame.draw.rect(surface, (255,0,0), pygame.Rect( x_rect_formula ))

        if self.dx > 0:
            # Get the leftmost block
            leftmost_block = self.get_nearest_block(direction="left",collided_blocks=x_collided)
            self.entity_collition_type["left-block"] = leftmost_block

            if leftmost_block != None:
                self.entity_collition_type["right"] = True # It colliderected with the right part of the hitbox's entity

        elif self.dx < 0:
            # Get therightmost block
            rightmost_block = self.get_nearest_block(direction="right",collided_blocks=x_collided)
            self.entity_collition_type["right-block"] = rightmost_block

            if rightmost_block != None:
                self.entity_collition_type["left"] = True # It colliderected with the left part of the hitbox's entity


    def y_physics(self, every_block_list, surface, screen_pos):
        # Check Y collition 
        # Try to predict the next two movements
        if self.dy >= 0:
            y_rect_formula = (screen_pos[0], screen_pos[1]  , self.hitbox_size[0], self.hitbox_size[1] + self.dy)
        elif self.dy < 0:
            y_rect_formula = (screen_pos[0], screen_pos[1] + self.dy , self.hitbox_size[0], self.hitbox_size[1] - self.dy)

        y_collided = self.collided_block_tiles(blocks_list=every_block_list, 
                                                    rect_formula=y_rect_formula)
        
        if self.dy > 0: # If the collision is going up
            # Get the highest block
            highest_block = self.get_nearest_block(direction="up", collided_blocks=y_collided)
            self.entity_collition_type["top-block"] = highest_block

            if highest_block != None:
                self.entity_collition_type["bottom"] = True

        elif self.dy < 0: # If the collision is going down
            # Get the lowest block
            lowest_block = self.get_nearest_block(direction="bottom", collided_blocks=y_collided)
            self.entity_collition_type["bottom-block"] = lowest_block

            if lowest_block != None:
                self.entity_collition_type["top"] = True # good

        #pygame.draw.rect(surface, (0,0,255), pygame.Rect( y_rect_formula ))

    def applyX_physics_changes(self):
        if self.entity_collition_type["right"]: 
            if self.entity_collition_type["left-block"] != None:
                self.dx = (self.entity_collition_type["left-block"].getHitbox().left) - pygame.Rect(self.screen_entity_hitbox).right
                

        elif self.entity_collition_type["left"]: 
            if self.entity_collition_type["right-block"] != None:
                self.dx = (self.entity_collition_type["right-block"].getHitbox().right) - pygame.Rect(self.screen_entity_hitbox).left
    
        # Reset dx and set return_dx
        self.return_dx = self.dx
        self.dx = 0

    def applyY_physics_changes(self):
        if self.entity_collition_type["bottom"]: 
            if self.entity_collition_type["top-block"] != None:
                self.dy = (self.entity_collition_type["top-block"].getHitbox().top) - pygame.Rect(self.screen_entity_hitbox).bottom
                self.vel_y = 0

        elif self.entity_collition_type["top"]: 
            if self.entity_collition_type["bottom-block"] != None:
                self.dy = (self.entity_collition_type["bottom-block"].getHitbox().bottom) - pygame.Rect(self.screen_entity_hitbox).top
                self.jumping = False

    def move_x(self, force): 
        self.dx = force



class PhysicsHandler:
    def __init__(self):
        self.gravity = 9.8