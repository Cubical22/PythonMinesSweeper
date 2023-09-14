from globalVal import cells, CELLCOUNT

def checkForWinState():
    for y in range(CELLCOUNT):
        for x in range(CELLCOUNT):
            if cells[x][y].cellHiddenState == 0 and cells[x][y].cellState == 0: # an empty cell not discovered
                return  False
    return True
