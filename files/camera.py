
class Camera:
    def __init__(self, init_xy, camera_size):
        self.xy = init_xy
        self.camera_size = camera_size

        self.updateWaitList = {"X": [], "Xtype": "SET",
                                "Y": [], "Ytype": "SET"}
        self.UpdateValues()
    def set_x_coord(self, value:int):
        self.__setcoords__("X", value)

    def set_y_coord(self, value:int):
        self.__setcoords__("Y", value)

    def add_to_x_coord(self, value):
        self.__addToCoords__("X", value)

    def add_to_y_coord(self, value):
        self.__addToCoords__("Y", value)

    def __setcoords__(self,index, value):
        # Set value
        self.updateWaitList[index] = [] # Reset the X/Y list
        self.updateWaitList[f"{index}type"] = "SET"
        self.updateWaitList[index].append(value)

    def __addToCoords__(self, index, value):
        # Add the value to a list, so it can be added to the xy variable later
        self.updateWaitList[index] = []
        self.updateWaitList[f"{index}type"] = "ADD"
        self.updateWaitList[index].append(value)

    def UpdateValues(self):
        for x in range(len(self.updateWaitList["X"])):
            if self.updateWaitList["Xtype"] == "ADD":
                self.xy[0] += self.updateWaitList["X"][x]

            elif self.updateWaitList["Xtype"] == "SET":
                self.xy[0] = self.updateWaitList["X"][0]
                break

        for y in range(len(self.updateWaitList["Y"])):
            if self.updateWaitList["Ytype"] == "ADD":
                self.xy[1] += self.updateWaitList["Y"][y]

            elif self.updateWaitList["Ytype"] == "SET":
                self.xy[1] = self.updateWaitList["Y"][0]
                break

        # Reset the list
        self.updateWaitList["X"] = []
        self.updateWaitList["Y"] = []

    def get_xy(self):
        return tuple(self.xy)

    def get_camera_size(self):
        return self.camera_size

    def convert_screen_pos_to_camera_xy(self, screen_pos):
        """ Does not work in some cases """
        return (screen_pos[0] - self.xy[0]), (screen_pos[1] - self.xy[1])
