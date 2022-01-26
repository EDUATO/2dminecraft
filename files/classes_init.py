import pygame

from files.vars import modeX, modeY
from files.terrain_generator import generate, seed, generation_loop, chunks_list
from files.import_imp import Blocks_texture, Player_texture
from files.debugScreen import DebugScreen
from files.camera import Camera
from files.player import Player
from files.Entity_manager import Entities
from files.functions import convert_blocks_pos_to_camera_xy

# Camera
CameraMain = Camera(init_xy=[0,0], camera_size=[modeX, modeY])

coords_to_spawn_cam = convert_blocks_pos_to_camera_xy(grid_pos=(4,20))

CameraMain.set_x_coord(coords_to_spawn_cam[0])
CameraMain.set_y_coord(coords_to_spawn_cam[1])

ActiveChunks = [] # Chunks that are active and will be updated

Entities_man = Entities(CameraMain)

# PLAYER'S
p1 = Entities_man.GetEntityClass(Entityid=1)

debug_screen = DebugScreen()

pygame.mouse.set_visible(False) # Hide cursor

selected_block = None # The block that is selected by the cursor (probably it will be removed later)