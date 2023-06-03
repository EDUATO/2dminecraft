
from files.entity.player import Player

from files.entity.w_ty import Wty



class Entities:
    def __init__(self, App, CameraMain, id=1):
        self.EntitiesTypes = {
            "Player":{"class":Player, "texture":App.assets.Player_texture},
            "Wty":{"class":Wty, "texture":App.assets.Wty_texture}}

        self.EntitiesInGame = []
        self.ActiveEntities = []

    def spawnEntity(self,App, CameraMain, type, Blockpos, custom_uuid=False, physics=True, bot=False):
        """ It will spawn an Entity and return its UUID """

        self.EntitiesInGame.append(self.EntitiesTypes[type]["class"](
                                                                App=App,
                                                                texture=self.EntitiesTypes[type]["texture"],
                                                                block_pos=Blockpos,
                                                                Camera=CameraMain,
                                                                custom_uuid=custom_uuid,
                                                                physics=physics,
                                                                bot=bot)
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
