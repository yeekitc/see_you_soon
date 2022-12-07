#################################################
# matrix.py
#
# Your name: Yee Kit Chan
# Your andrew id: yeekitc
#################################################

import math, os, copy, decimal, datetime, random, ast
from cmu_112_graphics import *
from button import *
import module_manager
module_manager.review()

class Matrix:
    def __init__(self, x0, y0, x1, y1, days=["sun", "mon", "tues", "weds", "thurs", "fri", "sat"], 
            times=[9, 10, 11, 12, 13, 14, 15, 16, 17], marginX=5, marginY=5, matrix=[]):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.rows = len(times)*2
        self.cols = len(days)
        if marginX==5:
            self.marginX = (x1-x0)/self.cols
        else:
            self.marginX = marginX
        if marginY==5:
            self.marginY = (y1-y0)/self.rows
        else:
            self.marginY = (y1-y0)/self.rows

        self.days = days
        self.times = times
        
        if matrix==[]:
            self.matrix = [[0]*self.cols for r in range(self.rows)]
        else:
            self.matrix = matrix

        self.clicked = False
        self.clickR = -1
        self.clickC = -1
        self.dragged = False
        self.dragX0 = -1
        self.dragY0 = -1
        self.dragX1 = -1
        self.dragY1 = -1
        self.hoverR = -1
        self.hoverC = -1

    def __repr__(self):
        return f'Matrix(x0={self.x0}, y0={self.y0}, x1={self.x1}, y1={self.y1}, marginX={self.marginX},\
            marginY={self.marginY}, days={self.days}, times={self.times}, matrix={self.matrix})'

    # resetting the drag variables
    def resetDrag(self):
        self.dragX0 = -1
        self.dragY0 = -1
        self.dragX1 = -1
        self.dragY1 = -1
        self.dragged = False

    # sets the dimensions of the availability matrix
    def setMatrixCoords(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.marginX = (x1-x0)/self.cols
        self.marginY = (y1-y0)/self.rows

    # sets the rows and cols of the availability matrix
    def setMatrixDims(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.marginX = (self.x1-self.x0)/cols
        self.marginY = (self.y1-self.y0)/rows

    # sets the possible days
    def setDays(self, dayList):
        self.days = dayList

    # sets the possible times
    def setTimes(self, timeList):
        self.times = timeList

    def onClick(self, event):
        if not self._pointInGrid(event.x, event.y):
            return False
        self.clicked = True
        self.clickR, self.clickC = self._getCell(event.x, event.y)
        if not self.dragged:
            if self.matrix[self.clickR][self.clickC] == 0:
                self.matrix[self.clickR][self.clickC] = 1
            else:
                self.matrix[self.clickR][self.clickC] = 0
        return True

    def onHover(self, event):
        if not self._pointInGrid(event.x, event.y):
            return False
        self.hoverR, self.hoverC = self._getCell(event.x, event.y)
        if self.dragged:
            if self.matrix[self.hoverR][self.hoverC] == 0:
                self.matrix[self.hoverR][self.hoverC] = 1
            else:
                self.matrix[self.hoverR][self.hoverC] = 0
        return True
    
    def onDrag(self, event):
        if not self._pointInGrid(event.x, event.y):
            return False
        self.dragged = True
        x, y = self._getCell(event.x, event.y)
        if self.dragX0==-1:
            self.dragX0 = x
        elif x > self.dragX0:
            self.dragX1 = x
        if self.dragY0==-1:
            self.dragY0 = y
        elif y > self.dragY0:
            self.dragY1 = y
        if self.dragX1==-1:
            self.dragX1 = self.dragX0+1
        if self.dragY1==-1:
            self.dragY1 = self.dragY0+1
        # if x==self.dragX0:
        #     self.dragX1 = self.dragX0
        # elif self.dragX1==-1 and x != self.dragX0:
        #     self.dragX1 = self.dragX0+1
        # if y==self.dragX0:
        #     self.dragY1 = self.dragY0
        # elif self.dragY1==-1  and y != self.dragY0:
        #     self.dragY1 = self.dragY0+1
        print(self.dragX0, self.dragY0, self.dragX1, self.dragY1)
        return True

    def onRelease(self, event):
        if not self._pointInGrid(event.x, event.y):
            return False
        r, c = self._getCell(event.x, event.y)
        for row in range(self.dragX0, self.dragX1):
            for col in range(self.dragY0, self.dragY1):
                if self.clicked:
                    self.clicked = False
                    continue
                if self.matrix[row][col] == 0:
                    self.matrix[row][col] = 1
                else:
                    self.matrix[row][col] = 0
        if not (r==self.clickR and c==self.clickC):
            if self.matrix[r][c] == 0:
                self.matrix[r][c] = 1
            else:
                self.matrix[r][c] = 0
        self.resetDrag()
        return True
    
    # modified from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
    def _pointInGrid(self, x, y):
        # return True if (x, y) is inside the grid defined by app.
        return ((self.marginX+self.x0 <= x <= self.x1-self.marginX) and
                (self.marginY+self.y0 <= y <= self.y1-self.marginY))

    # modified from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
    def _getCell(self, x, y):
        # aka "viewToModel"
        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        if (not self._pointInGrid(x, y)):
            return (-1, -1)
        gridWidth  = (self.x1-self.x0) - 2*self.marginX
        gridHeight = (self.y1-self.y0) - 2*self.marginY
        cellWidth  = gridWidth / self.cols
        cellHeight = gridHeight / self.rows

        # Note: we have to use int() here and not just // because
        # row and col cannot be floats and if any of x, y, app.margin,
        # cellWidth or cellHeight are floats, // would still produce floats.
        row = int((y - self.marginY - self.y0) / cellHeight)
        col = int((x - self.marginX - self.x0) / cellWidth)

        return (row, col)

    # modified from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
    def _getCellBounds(self, row, col):
        # print("new", self)
        # aka "modelToView"
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        gridWidth  = (self.x1-self.x0) - 2*self.marginX
        gridHeight = (self.y1-self.y0) - 2*self.marginY
        cellWidth = gridWidth / self.cols
        cellHeight = gridHeight / self.rows
        # print("new", gridWidth, gridHeight, cellWidth, cellHeight)
        x0 = self.x0 + self.marginX + col * cellWidth
        x1 = self.x0 + self.marginX + (col+1) * cellWidth
        y0 = self.y0 + self.marginY + row * cellHeight
        y1 = self.y0 + self.marginY + (row+1) * cellHeight
        # print("new", x0, y0, x1, y1)
        return (x0, y0, x1, y1)

    # translates the availability matrix integers to colors
    def _intToGradient(self, gradient):
        rows = len(self.matrix)
        cols = len(self.matrix[0])
        gradientMatrix = [[""]*cols for r in range(rows)]
        for r in range(rows):
            for c in range(cols):
                colorIndex = self.matrix[r][c]
                if r==self.hoverR and c==self.hoverC:
                    colorIndex += 1
                gradientMatrix[r][c] = gradient[colorIndex]
        return gradientMatrix

    # draws matrix based on possible days (currently default 7) & times (default 9-5)
    def drawMatrix(self, app, canvas):
        # https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
        for row in range(self.rows):
            for col in range(self.cols):
                (x0, y0, x1, y1) = self._getCellBounds(row, col)
                fill = self._intToGradient(app.availGradient)[row][col]
                canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
        self.drawMatrixLabels(app, canvas)

    # draws labels on the horizontal & vertical axes of the availability matrix
    def drawMatrixLabels(self, app, canvas):
        gridWidth  = (self.x1-self.x0) - 2*self.marginX
        gridHeight = (self.y1-self.y0) - 2*self.marginY
        cellWidth = gridWidth / self.cols
        cellHeight = gridHeight / self.rows
        font = "Open Sans", f"{int(cellHeight/2)}", "bold"
        for day in range(len(self.days)):
            canvas.create_text(self.marginX+self.x0+cellWidth/2+cellWidth*day, self.y0+cellHeight/2, 
                            text=self.days[day], fill=app.textC, font=font)
        for time in range(len(self.times)):
            meridiem = ""
            text = ""
            if self.times[time] > 12:
                meridiem = " PM"
            else:
                meridiem = " AM"
            if self.times[time]%12 == 0:
                text = "12" + meridiem
            else:
                text = f"{self.times[time]%12}" + meridiem
            canvas.create_text(self.x0+cellWidth/2, self.marginY+self.y0+cellHeight*(2*time+1),
                            text=text, fill=app.textC, font=font)

class EventMatrix(Matrix):
    def __init__(self, x0, y0, x1, y1, days=["sun", "mon", "tues", "weds", "thurs", "fri", "sat"], 
            times=[9, 10, 11, 12, 13, 14, 15, 16, 17], marginX=5, marginY=5, matrix=[]):
            self.enableRec = False
            self.recR, self.recC = -1, -1
            super().__init__(x0, y0, x1, y1, days=days, times=times, 
                marginX=marginX, marginY=marginY, matrix=matrix)
    
    def __repr__(self):
        return f'EventMatrix(x0={self.x0}, y0={self.y0}, x1={self.x1}, y1={self.y1}, marginX={self.marginX},\
            marginY={self.marginY}, days={self.days}, times={self.times}, matrix={self.matrix})'

    def onHover(self, event):
        if not self._pointInGrid(event.x, event.y):
            return (False, -1, -1)
        self.hoverR, self.hoverC = self._getCell(event.x, event.y)
        return (True, self.hoverR, self.hoverC)

    # translates the availability matrix integers to colors
    def _intToGradient(self, gradient):
        rows = len(self.matrix)
        cols = len(self.matrix[0])
        gradientMatrix = [[""]*cols for r in range(rows)]
        for r in range(rows):
            for c in range(cols):
                colorIndex = self.matrix[r][c]
                if r==self.hoverR and c==self.hoverC:
                    colorIndex += 1
                if self.enableRec and r==self.recR and c==self.recC:
                    gradientMatrix[r][c] = "#FA8072"
                else:
                    gradientMatrix[r][c] = gradient[colorIndex]
        return gradientMatrix