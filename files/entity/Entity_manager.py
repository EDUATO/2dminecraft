
from files.entity.player import Player
from files.import_imp import Player_texture

EntitiesTypes = {"Player":{"class":Player, "texture":Player_texture}}

class Entities:
    def __init__(self, CameraMain, id=1):
        self.EntitiesInGame = []
        self.ActiveEntities = []

    def spawnEntity(self, CameraMain, type, Blockpos, custom_uuid=False):
        """ It will spawn an Entity and return its UUID """

        self.EntitiesInGame.append(EntitiesTypes[type]["class"](
                                                                texture=EntitiesTypes[type]["texture"],
                                                                pos=Blockpos,
                                                                Camera=CameraMain,
                                                                custom_uuid=custom_uuid)
                                                                )

        return self.EntitiesInGame[len(self.EntitiesInGame)-1].get_uuid()

    def getEntitiesClasses(self):
        classes = []
        for i in range(len(self.EntitiesInGame)):
            classes.append(self.EntitiesInGame[i])

        return classes

    def GetEntityClass(self, Entityid):
        output = None
        for i in range(len(self.EntitiesInGame)):
            if self.EntitiesInGame[i].get_uuid()== Entityid:
                output = self.EntitiesInGame[i]
                break

        return output

    def updateEntitiesCamera(self, CameraMain):
        for i in range(len(self.EntitiesInGame)):
            self.EntitiesInGame[i].camera_updater(Camera=CameraMain)

    def entities_in_game_amount(self): return len(self.EntitiesInGame)
