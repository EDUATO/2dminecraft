import pygame
import threading

from files.vars import modeX, modeY, chunk_size
from files.terrain.terrain_generator import generate, seed, chunks_list, chunk_manager_list
from files.import_imp import Blocks_texture, Player_texture
from files.debugScreen import DebugScreen
from files.camera import Camera
from files.entity.player import Player
from files.entity.Entity_manager import Entities
from files.functions import convert_blocks_pos_to_camera_xy, detect_chunk_with_position
from files.saving.saveload import read_save_files

class Game_Initialization:
    def __init__(self):
        self.CameraMain = Camera(init_xy=[0,0], camera_size=[modeX, modeY])

        self.initialization_progress = 0
        self.full_initialation = False

        self.chunks_list = chunks_list

        self.init_entities()

    def init_blocks(self):
        if not self.full_initialation:
            #self.chunks_list = read_save_files(chunks_list=self.chunks_list)
            
            self.check_if_full_initialization()
        else:
            self.__error_code__()

    def init_entities(self):
        global chunk_manager_list
        if not self.full_initialation:
            self.coords_to_spawn_cam = convert_blocks_pos_to_camera_xy(grid_pos=(4,20))

            self.CameraMain.set_x_coord(self.coords_to_spawn_cam[0])
            self.CameraMain.set_y_coord(self.coords_to_spawn_cam[1])

            self.ActiveChunks = [] # Chunks that are active and will be updated

            self.Entities_man = Entities(self.CameraMain)

            # Spawn player
            player_initial_pos = (5, 40)
            self.p1_uuid = self.Entities_man.spawnEntity(self.CameraMain, type="Player", Blockpos=player_initial_pos)

            """for i in range(2):
                self.Entities_man.spawnEntity(self.CameraMain, type="Player", Blockpos=(2*(i+1), 40))"""

            # PLAYER'S
            self.p1 = self.Entities_man.GetEntityClass(Entityid=self.p1_uuid)
            self.check_if_full_initialization()
        
        else:
            self.__error_code__()

    def init_screen(self):
        if not self.full_initialation:
            self.debug_screen = DebugScreen()

            self.show_debug_screen = False

            pygame.mouse.set_visible(False) # Hide cursor

            self.selected_block = None # The block that is selected by the cursor (probably it will be removed later)

            self.check_if_full_initialization()
        else:
            self.__error_code__()

    def check_if_full_initialization(self):
        self.initialization_progress += 1
        if self.initialization_progress >= 3:
            print("full init")
            self.full_initialation = True

    def reset_initialization(self):
        self.initialization_progress = 0
        self.full_initialation = False

    def __error_code__(self):
        print("Already initialized")