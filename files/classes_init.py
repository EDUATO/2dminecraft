import pygame
import threading

from files.terrain_generator import generate, chunk_blocks_list, seed, generation_loop
from files.import_imp import Blocks_texture, Player_texture
from files.debugScreen import DebugScreen
from files.camera import Camera
from files.gui.hotbar import Hotbar
from files.gui.Inventory import Inventory
from files.player import Player

# Camera
CameraMain = Camera(init_xy=[0,0])

# TERRAIN GENERATOR
loop = threading.Thread(target=generation_loop, daemon=True, args=[CameraMain]) # It destroys when the main thread ends
loop.start()

ActiveChunks = [chunk_blocks_list[0]] # Chunks that are active and will be updated

# PLAYER'S
p1 = Player(Player_texture, ("m", 0), Camera=CameraMain, Camera_Focus=True) # Main player

PlayerInventory = Inventory()

Player_Hotbar = Hotbar()

# ENTITIES
EntitiesInGame = []

for a in range(2):
	EntitiesInGame.append(Player(Player_texture, ((40)*(a+2), 193),Camera=CameraMain, Camera_Focus=False ))


debug_screen = DebugScreen()

pygame.mouse.set_visible(False) # Hide cursor

selected_block = None # The block that is selected by the cursor (probably it will be removed later)