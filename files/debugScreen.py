import pygame
import files.functions as f

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
            f.text(surface, self.DebugList[i]["text"], 20, y, Arial_30, self.DebugList[i]["color"])
            y += 50

    def resetDebugList(self):
        self.DebugList = []