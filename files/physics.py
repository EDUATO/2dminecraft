import pygame
from pygame.locals import *


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
        
        self.entity_collition_type = {"right":False, "left":False, "bottom":False, "top":False} #Player's hitbox collition
    def update(self, chunks_list, surface, screen_pos, deltaTime=1):
        self.reload_diferences()
        # Gravity
        self.vel_y = self.update_gravity(self.vel_y)
        self.dy += (self.vel_y * deltaTime)

        self.screen_entity_hitbox = (screen_pos[0], screen_pos[1], self.hitbox_size[0], self.hitbox_size[1])

        # Get blocks near the entity
        collided_blocks = self.nearbyblocks(chunks_list, self.screen_entity_hitbox)


        # X PHYSICS
        self.x_physics(collided_blocks, surface, screen_pos)

        # Y PHYSICS
        self.y_physics(collided_blocks, surface, screen_pos)

        
        #self.dx = 0
    def update_gravity(self, vel_y:int, deltaTime=1):
        vel_y += (1 * deltaTime)
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
        for j in range(len(collided_blocks)):
            block = collided_blocks[j] # Blocks that the entity collided

            if direction == "left" or direction == "right":
                index = 0 # x coords
            elif direction == "up" or direction == "bottom":
                index = 1 # y coords
            
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

        pygame.draw.rect(surface, (255,0,0), pygame.Rect( x_rect_formula ))

        if self.dx > 0:
            # Get the leftmost block
            leftmost_block = self.get_nearest_block(direction="left",collided_blocks=x_collided)

            if leftmost_block != None:
                self.dx = (leftmost_block.getHitbox().left) - pygame.Rect(self.screen_entity_hitbox).right
                self.entity_collition_type["right"] = True # It colliderected with the right part of the hitbox's entity

        elif self.dx < 0:
            # Get therightmost block
            rightmost_block = self.get_nearest_block(direction="right",collided_blocks=x_collided)

            if rightmost_block != None:
                self.dx = (rightmost_block.getHitbox().right) - pygame.Rect(self.screen_entity_hitbox).left
                self.entity_collition_type["left"] = True # It colliderected with the left part of the hitbox's entity

        # Reset dx and set return_dx
        self.return_dx = self.dx
        self.dx = 0


    def y_physics(self, every_block_list, surface, screen_pos):
        # Check Y collition 
        # Try to predict the next movement
        if self.dy >= 0:
            y_rect_formula = (screen_pos[0], screen_pos[1] , self.hitbox_size[0], self.hitbox_size[1] + self.dy)
        elif self.dy < 0:
            y_rect_formula = (screen_pos[0], screen_pos[1] + self.dy , self.hitbox_size[0], self.hitbox_size[1] - self.dy)

        y_collided = self.collided_block_tiles(blocks_list=every_block_list, 
                                                    rect_formula=y_rect_formula)
        
        if self.dy > 0: # If the collision is going up
            # Get the highest block
            highest_block = self.get_nearest_block(direction="up", collided_blocks=y_collided)

            if highest_block != None:
                self.dy = highest_block.getHitbox().top - pygame.Rect(self.screen_entity_hitbox).bottom
                self.vel_y = 0
                self.entity_collition_type["bottom"] = True

        elif self.dy < 0: # If the collision is going down
            # Get the lowest block
            lowest_block = self.get_nearest_block(direction="bottom", collided_blocks=y_collided)

            if lowest_block != None:
                self.dy = lowest_block.getHitbox().bottom - pygame.Rect(self.screen_entity_hitbox).top
                self.jumping = False
                self.entity_collition_type["top"] = True # good
            
        pygame.draw.rect(surface, (0,0,255), pygame.Rect( y_rect_formula ))

    def move_x(self, force):
        self.dx = force