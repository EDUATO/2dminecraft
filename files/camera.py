
class Camera:
    def __init__(self, init_xy):
        self.xy = init_xy

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