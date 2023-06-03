import pygame

from files.gui.Text import Text

class DebugScreen:
    def __init__(self):
        self.activated = False
        self.DebugList = []

    def Show(self, App):
        self.WriteTexts(App)

    def addDebugText(
        self,
        text,
        color):

        self.DebugList.append(
            {"text":str(text),
            "color":color}
        )

    def WriteTexts(self, App):
        y = 10
        for i in range(len(self.DebugList)):
            debugText = Text(20, y, self.DebugList[i]["text"], App.assets.Mc_15, self.DebugList[i]["color"])
            debugText.draw(App)

            y += 30

    def resetDebugList(self):
        self.DebugList = []