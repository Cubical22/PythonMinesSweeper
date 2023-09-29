from globalVal import cells, CELLCOUNT

def cellReveal(selectedCellPos):
    outsideX = 0
    outsideY = 0

    if selectedCellPos[0] - 2 < 0:
        outsideX = 2 - selectedCellPos[0]
    elif selectedCellPos[0] + 2 > CELLCOUNT - 1:
        outsideX = (CELLCOUNT - 1 - selectedCellPos[0]) - 2

    if selectedCellPos[1] - 2 < 0:
        outsideY = 2 - selectedCellPos[1]
    elif selectedCellPos[1] + 2 > CELLCOUNT - 1:
        outsideY = (CELLCOUNT - 1 - selectedCellPos[1]) - 2

    for y in range(selectedCellPos[1] + outsideY - 2, selectedCellPos[1] + outsideY + 3):
        for x in range(selectedCellPos[0] + outsideX - 2, selectedCellPos[0] + outsideX + 3):
            cells[y][x].revealSelf()