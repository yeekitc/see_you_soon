#################################################
# fakeinit.py
#
# Your name: Yee Kit Chan
# Your andrew id: yeekitc
#################################################

import math, os, copy, decimal, datetime
from cmu_112_graphics import *
import module_manager
module_manager.review()

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Tetris
#################################################
def gameDimensions():
    # These values are set to the writeup defaults
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return (rows, cols, cellSize, margin)

# stores the model/data needed for Tetris
def appStarted(app):
    # app.emptyColor = "white"
    # app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    # app.board = [([app.emptyColor]*app.cols) for row in range(app.rows)]
    pass

# controller
def keyPressed(app, event):
    pass

# controller; based on timer
def timerFired(app):
    pass

def mousePressed(app, event):
    pass
    
def mouseDragged(app, event):
    if app.pressedScroll is not None:
        app.toolboxScroll = min(0, app.pressedScroll + dy)

def mouseReleased(app, event):
    pass

# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCellBounds(app, row, col):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)

# draws the board
def drawAvailabilityMatrix(app, canvas):
    # draw grid of cells
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, canvas, row, col, app.board[row][col])

# draws the cell in color
def drawCell(app, canvas, row, col, color):
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1, fill=color, 
                            outline="dim gray", width=2)

def drawScrollbar(app, canvas):
    scrollbarHeight = app.height*(app.height / app.toolboxExtent)

    maxScroll = app.toolboxExtent - app.height
    maxScrollbarMove = app.height - scrollbarHeight
    scrollBarY = maxScrollbarMove*(-app.toolboxScroll/maxScroll)

    scrollBarY0 = min(scrollBarY, maxScrollbarMove)

    canvas.create_rectangle(
        app.width-app.scrollbarWidth, scrollBarY0,
        app.width, scrollBarY0+scrollbarHeight,
        fill='light gray', outline='')

# view
def redrawAll(app, canvas):
    # background
    canvas.create_rectangle(0, 0, app.width, app.height, fill="MistyRose4")
    drawAvailabilityMatrix(app, canvas)

# runs see_you_soon
def runSeeYouSoon():
    rows, cols, cellSize, margin = gameDimensions()
    width = cols*cellSize + 2*margin
    height = rows*cellSize + 2*margin
    runApp(width=width, height=height)

runSeeYouSoon()