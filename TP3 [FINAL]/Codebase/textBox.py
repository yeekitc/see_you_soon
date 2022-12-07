#################################################
# textBox.py
#
# Your name: Yee Kit Chan
# Your andrew id: yeekitc
#################################################

import string
from cmu_112_graphics import *
import module_manager
module_manager.review()

# TextBox class
class TextBox:
    def __init__(self, x0, y0, x1, y1, textC="#143936", bgC="#FFFFFF", outlineC="#143936", selectC="#9FF8E2", bgText="", bgTextC="#91a3a3", hidden=False):
        self.x0 = x0            # x0 when drawn
        self.y0 = y0            # y0 when drawn
        self.x1 = x1            # x1 when drawn
        self.y1 = y1            # y1 when drawn
        self.bgText = bgText    # background text prompt for the textbox
        self.inText = ""        # user input
        self.selected = False   # whether the textbox is selected
        self.hover = False      # whether the textbox is hovered over

        self.cursor = False     # whether the cursor is shown
        self.hidden = hidden    # whether the inputted text will be masked 

        # colors
        self.textC = textC
        self.bgC = bgC
        self.bgTextC = bgTextC
        self.outlineC = outlineC
        self.selectC = selectC

    # returns the user input
    def getText(self):
        return self.inText

    # sets the background text prompt for the TextBox
    def setBgText(self, bgText):
        self.bgText = bgText

    # controls the blinking cursor according to time
    def cursorBlink(self):
        # toggle the cursor only if the TextBox is selected
        if self.selected:
            self.cursor = not self.cursor
        else:
            self.cursor = False

    # if click within the TextBox, set self.selected to True
    def onClick(self, app, event):
        x, y = event.x, event.y
        if x>=self.x0 and x<=self.x1 and y>=self.y0 and y<=self.y1:
            self.selected = True
        else:
            self.selected = False

    # if hover within the TextBox, set self.hover to True
    def onHover(self, event):
        x, y = event.x, event.y
        if x>=self.x0 and x<=self.x1 and y>=self.y0 and y<=self.y1:
            self.hover = True
        else:
            self.hover = False

    # store user input based on the keys pressed when the TextBox is selected
    def keysIn(self, event):
        if self.selected:
            # delete the last character from the user input when BackSpace pressed
            if event.key == "BackSpace":
                self.inText = self.inText[:-1]
            elif event.key == "Space":
                self.inText += " "
            elif event.key in {"-", "_", ".", "@", ",", "!", ".", "/", "'", '"'}:
                self.inText += event.key
            elif event.key in set(string.ascii_letters) or event.key in set(string.digits):
                self.inText += event.key

    # draws the TextBox
    def drawTextBox(self, app, canvas):
        width, height = self.x1-self.x0, self.y1-self.y0
        font = "Open Sans", f"{int(height/2)}"

        # create an accent-colored rectangle when the TextBox is selected/hovered over
        if self.selected or self.hover:
            canvas.create_rectangle(self.x0-5, self.y0-5, self.x1+5, self.y1+5, fill=self.selectC)

        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill=self.bgC, outline=self.outlineC)
        
        # if the TextBox is not selected and no user input, show background text prompt
        if not self.selected and self.inText == "":
            canvas.create_text(self.x0+10, self.y0+height/2, text=self.bgText, font=font, fill=self.bgTextC, anchor=W)
        # otherwise display the user input
        else:
            text = ""
            # if hidden, display text will be password dots
            if self.hidden:
                for char in self.inText:
                    text += "•"
            else:
                text += self.inText
            # if the cursor is on, add to the end of the display text
            if self.selected and self.cursor:
                text += " |"
            canvas.create_text(self.x0+10, self.y0+height/2, text=text, font=font, fill=self.textC, anchor=W)