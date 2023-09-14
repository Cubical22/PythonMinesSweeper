import random
from globalVal import *
from utils import checkInsideLength

def generateBombs():
    count = random.randint(8,13)
    for i in range(count):
        while True:
            y = random.randint(0,CELLCOUNT - 1)
            x = random.randint(0,CELLCOUNT - 1)
            if cells[x][y].cellHiddenState != 1: # not being a bomb
                cells[x][y].cellHiddenState = 1
                break

def updateAdjBombs():
    for y in range(CELLCOUNT):
        for x in range(CELLCOUNT):
            checkAdjBombs((x,y))

def checkAdjBombs(currentCellPos):
    cellWithOffset(currentCellPos, 1, 0)
    cellWithOffset(currentCellPos, -1, 0)
    cellWithOffset(currentCellPos, 0, 1)
    cellWithOffset(currentCellPos, 0, -1)

    cellWithOffset(currentCellPos, 1, 1)
    cellWithOffset(currentCellPos, 1, -1)
    cellWithOffset(currentCellPos, -1, 1)
    cellWithOffset(currentCellPos, -1, -1)

def cellWithOffset(currentCellPos, offX, offY):
    if not checkInsideLength(currentCellPos[0] + offX, currentCellPos[1] + offY, CELLCOUNT):
        return

    # add to the adj count incase if the state of the adj cell is a bomb
    adjCell = cells[currentCellPos[0] + offX][currentCellPos[1] + offY]
    if adjCell.cellHiddenState == 1: # the adj cell is a bomb
        cells[currentCellPos[0]][currentCellPos[1]].adjBombCount += 1