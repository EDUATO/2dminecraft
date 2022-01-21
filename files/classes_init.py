import pygame
import threading

from files.vars import modeX, modeY
from files.terrain_generator import generate, chunk_blocks_list, seed, generation_loop
from files.import_imp import Blocks_texture, Player_texture
from files.debugScreen import DebugScreen
from files.camera import Camera
from files.gui.hotbar import Hotbar
from files.gui.Inventory import Inventory
from files.player import Player
from files.functions import convert_blocks_pos_to_camera_xy

# Camera
CameraMain = Camera(init_xy=[0,0], camera_size=[modeX, modeY])

coords_to_spawn_cam = convert_blocks_pos_to_camera_xy(grid_pos=(4,20))

CameraMain.set_x_coord(coords_to_spawn_cam[0])
CameraMain.set_y_coord(coords_to_spawn_cam[1])


# TERRAIN GENERATOR
loop = threading.Thread(target=generation_loop, daemon=True, args=[CameraMain]) # It destroys when the main thread ends
loop.start()

ActiveChunks = [chunk_blocks_list[0]] # Chunks that are active and will be updated

# PLAYER'S
p1 = Player(Player_texture, (5, 20), Camera=CameraMain) # Main player

PlayerInventory = Inventory()

Player_Hotbar = Hotbar()

# ENTITIES
EntitiesInGame = []

for a in range(2):
	EntitiesInGame.append(Player(Player_texture, (15, 20),Camera=CameraMain))


debug_screen = DebugScreen()

pygame.mouse.set_visible(False) # Hide cursor

selected_block = None # The block that is selected by the cursor (probably it will be removed later)