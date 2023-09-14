from kivy.uix.button import Button
from cellExplore import exploreFromStart
from stateHandling import checkForWinState

class CellButton(Button):
    xIndex = 0
    yIndex = 0
    cellState = 0 # keeps track of whether the cell is discovered or not
    # 0: not discovered 1: discovered
    cellHiddenState = 0 # keeps track of the actual state of the cells
    # 0: empty 1: bomb
    adjBombCount = 0 # How many bombs on the surrounding cells

    def callCell(self, *args):
        # if the cell is a bomb
        if self.cellHiddenState == 1:
            print("you lost")
            self.background_color = (1,0,0,1) # DEBUGGING: this is only to debug the code
        else:
            if self.adjBombCount == 0:
                exploreFromStart(self.yIndex, self.xIndex) # for some reason I don't know, passing args as [x,y] is
                # not working, and is doing everything in reverse :)
                # passing it as [y,x] fixed our problem for now
            else: # this is a counted cell
                self.background_color = (1,1,1,1)
                self.cellState = 1 # explored
                self.text = str(self.adjBombCount)
                self.color = (0,0,0,1)

        isWinState = checkForWinState()

        if isWinState:
            print("you have won")