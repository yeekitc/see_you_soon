#################################################
# textBox.py
#
# Your name: Yee Kit Chan
# Your andrew id: yeekitc
#################################################

import math, os, copy, decimal, datetime, string
from cmu_112_graphics import *
import module_manager
module_manager.review()

class TextBox:
    def __init__(self, x0, y0, x1, y1, textC="#143936", bgC="#FFFFFF", outlineC="#143936", selectC="#9FF8E2", bgText="", bgTextC="#91a3a3", hidden=False):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.bgText = bgText
        self.inText = ""
        self.selected = False
        self.hover = False

        self.cursor = False
        self.hidden = hidden

        # colors
        self.textC = textC
        self.bgC = bgC
        self.bgTextC = bgTextC
        self.outlineC = outlineC
        self.selectC = selectC

    def getText(self):
        return self.inText

    def setBgText(self, bgText):
        self.bgText = bgText

    def cursorBlink(self):
        if self.selected:
            self.cursor = not self.cursor
        else:
            self.cursor = False

    def onClick(self, app, event):
        x, y = event.x, event.y
        if x>=self.x0 and x<=self.x1 and y>=self.y0 and y<=self.y1:
            self.selected = True
        else:
            self.selected = False

    def onHover(self, event):
        x, y = event.x, event.y
        if x>=self.x0 and x<=self.x1 and y>=self.y0 and y<=self.y1:
            self.hover = True
        else:
            self.hover = False
            
    def keysIn(self, event):
        if self.selected:
            if event.key == "BackSpace":
                self.inText = self.inText[:-1]
            elif event.key in {"-", "_", ".", "@"}:
                self.inText += event.key
            elif event.key in set(string.ascii_letters) or event.key in set(string.digits):
                self.inText += event.key

    def drawTextBox(self, app, canvas):
        width, height = self.x1-self.x0, self.y1-self.y0
        font = "Open Sans", f"{int(height/2)}"

        if self.selected or self.hover:
            canvas.create_rectangle(self.x0-5, self.y0-5, self.x1+5, self.y1+5, fill=self.selectC)

        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill=self.bgC, outline=self.outlineC)
        
        if not self.selected and self.inText == "":
            canvas.create_text(self.x0+10, self.y0+height/2, text=self.bgText, font=font, fill=self.bgTextC, anchor=W)
        else:
            text = ""
            if self.hidden:
                for char in self.inText:
                    text += "•"
            else:
                text += self.inText
            if self.selected and self.cursor:
                text += " |"
            canvas.create_text(self.x0+10, self.y0+height/2, text=text, font=font, fill=self.textC, anchor=W)