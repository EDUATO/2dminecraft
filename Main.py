from files.vars import modeX, modeY
from files.App import App

if __name__ == "__main__":
    a = App(dims=(modeX, modeY))
    a.update()