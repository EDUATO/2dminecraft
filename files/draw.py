import pygame
import threading

import pymunk
import pymunk.pygame_util

import files.Game as mg
from files.vars import Scene, win
from files.terrain.terrain_generator import generate, seed, generation_loop, Chunk_Manager_List
from files.menu.gameMenu import GameMenu

def set_collide_block_hitbox(hitbox):
	""" pymunk collide static surface """
	block_body = pymunk.Body(body_type=pymunk.Body.STATIC)
	block_body.position = (hitbox[0] + hitbox[2]/2, hitbox[1] + hitbox[3]/2)
	rect_size = (hitbox[2], hitbox[3])
	shape = pymunk.Poly.create_box(block_body, rect_size)

	shape.color = (100, 100,200, 1)
	shape.elasticity = 0.4
	shape.friction = 0.5

	return shape

def set_dynamic_circle():
	body = pymunk.Body()
	body.position = (300, 300)
	shape = pymunk.Circle(body, 20)
	shape.mass = 30
	# Add elasticity and friction
	shape.elasticity = 2
	shape.friction = 0.5

	shape.color = (255, 0, 0, 100)

	return shape


# TERRAIN GENERATOR
loop = threading.Thread(target=generation_loop, daemon=True) # It destroys when the main thread ends
loop.start()

mainMenu = GameMenu()

initialChunksGenerated = False

Game_Main_Class = None

""" Physics test """
espais = pymunk.Space()
espais.gravity = (0, 900)

shape = set_dynamic_circle()
espais.add(shape, shape.body)

hitbox = set_collide_block_hitbox(hitbox=(100,500,700,100))
espais.add(hitbox, hitbox.body)


drawOptions = pymunk.pygame_util.DrawOptions(win)
def Draw(surface, events, deltaTime=1):
	
	
	global initialChunksGenerated, Game_Main_Class
	if Scene == "game":
		if initialChunksGenerated:
			Game_Main_Class.update(events, surface)

		else:
			if Chunk_Manager_List == []:
				initialChunksGenerated = True
				Game_Main_Class = mg.Game()

	elif Scene == "main_menu":
		mainMenu.show(surface)

	""" Physics test """
	espais.debug_draw(drawOptions)
	if initialChunksGenerated:
		espais.step(deltaTime)
	
	


	