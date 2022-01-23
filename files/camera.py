
class Camera:
    def __init__(self, init_xy, camera_size):
        self.xy = init_xy
        self.camera_size = camera_size

    def set_x_coord(self, value:int, addToTheVar:bool=False):
        self.__setcoords__(0, value, addToTheVar=addToTheVar)

    def set_y_coord(self, value:int, addToTheVar:bool=False):
        self.__setcoords__(1, value, addToTheVar=addToTheVar)

    def __setcoords__(self,index, value, addToTheVar=False):
        if addToTheVar:
            # Add value to the y var
            self.xy[index] += value
            return self.xy[index]

        # Set the y var according to value
        self.xy[index] = value
        return self.xy[index]

    def get_xy(self):
        return tuple(self.xy)

    def get_camera_size(self):
        return self.camera_size

    def convert_screen_pos_to_camera_xy(self, screen_pos):
        """ Does not work in some cases """
        return (screen_pos[0] - self.xy[0]), (screen_pos[1] - self.xy[1])
