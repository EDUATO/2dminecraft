
from files.player import Player
from files.import_imp import Player_texture

EntitiesTypes = {"Player":{"class":Player, "texture":Player_texture}}

class Entities:
    def __init__(self, CameraMain, id=0):
        self.EntitiesInGame = []
        self.ActiveEntities = []

        self.spawnEntity(CameraMain=CameraMain, type="Player", Blockpos=(5, 20), EntityId=id)
        self.spawnEntity(CameraMain=CameraMain, type="Player", Blockpos=(10, 20), EntityId=1)

    def spawnEntity(self, CameraMain, type, Blockpos, EntityId):
        self.EntitiesInGame.append(EntitiesTypes[type]["class"](
                                                                texture=EntitiesTypes[type]["texture"],
                                                                pos=Blockpos,
                                                                Camera=CameraMain,
                                                                id=EntityId)
                                                                )

        print(self.EntitiesInGame)

    def getEntitiesClasses(self):
        classes = []
        for i in range(len(self.EntitiesInGame)):
            classes.append(self.EntitiesInGame[i])

        return classes

    def GetEntityClass(self, Entityid):
        output = None
        for i in range(len(self.EntitiesInGame)):
            if self.EntitiesInGame[i].get_id() == Entityid:
                output = self.EntitiesInGame[i]
                print("found")
                break

        return output
