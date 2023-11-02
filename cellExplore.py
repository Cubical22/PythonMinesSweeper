from globalVal import *
from utils import checkInsideLength
from kivy.app import App


def exploreFromStart(cellX, cellY):  # this function handles the exploration of cells that have an adj count > 0
    exploreNext = [[cellX, cellY]]

    while len(exploreNext) != 0:
        nextGen = []

        for (index, cell) in enumerate(exploreNext):
            exploreAdjCell(cell, nextGen)

        exploreNext = nextGen


def exploreAdjCell(cellPos, nextGen):
    if exploreWithOffset(cellPos, 1, 0): nextGen.append([cellPos[0] + 1, cellPos[1]])
    if exploreWithOffset(cellPos, -1, 0): nextGen.append([cellPos[0] - 1, cellPos[1]])
    if exploreWithOffset(cellPos, 0, 1): nextGen.append([cellPos[0], cellPos[1] + 1])
    if exploreWithOffset(cellPos, 0, -1): nextGen.append([cellPos[0], cellPos[1] - 1])
    if exploreWithOffset(cellPos, 0, 0): nextGen.append([cellPos[0], cellPos[1]])

    # diagonals
    if exploreWithOffset(cellPos, 1, 1): nextGen.append([cellPos[0] + 1, cellPos[1] + 1])
    if exploreWithOffset(cellPos, 1, -1): nextGen.append([cellPos[0] + 1, cellPos[1] - 1])
    if exploreWithOffset(cellPos, -1, 1): nextGen.append([cellPos[0] - 1, cellPos[1] + 1])
    if exploreWithOffset(cellPos, -1, -1): nextGen.append([cellPos[0] - 1, cellPos[1] - 1])

def exploreWithOffset(cellPos, offX, offY):
    if not checkInsideLength(cellPos[0] + offX, cellPos[1] + offY, CELLCOUNT):
        return False

    cell = cells[cellPos[0] + offX][cellPos[1] + offY]
    if cell.cellHiddenState == 1 or cell.cellState == 1:
        # this is a bomb, or it is discovered, or it is surrounded by bombs
        return False

    cell.cellState = 1 # explored
    cell.background_color = CELL_DISCOVER_COLOR

    if cell.adjBombCount != 0:
        cell.callCell()

    if not App.get_running_app().isInsideDialog:
        cell.checkDialog() # the possibility is calculated inside the button

    return cell.adjBombCount == 0
