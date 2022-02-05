import pygame

from files.gui.Text import Text
from files.fonts import *

class DebugScreen:
    def __init__(self):
        self.activated = False
        self.DebugList = []

    def Show(self, surface):
        self.WriteTexts(surface)

    def addDebugText(
        self,
        text,
        color):

        self.DebugList.append(
            {"text":str(text),
            "color":color}
        )

    def WriteTexts(self, surface):
        y = 10
        for i in range(len(self.DebugList)):
            debugText = Text(20, y, self.DebugList[i]["text"], Arial_30, self.DebugList[i]["color"])
            debugText.draw(surface)

            y += 50

    def resetDebugList(self):
        self.DebugList = []