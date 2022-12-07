#################################################
# button.py
#
# Your name: Yee Kit Chan
# Your andrew id: yeekitc
#################################################

import math, os, copy, decimal, datetime
from cmu_112_graphics import *
from event import *
import module_manager
module_manager.review()

# renamed with help from Piazza post @3177
class Bbutton:
    def __init__(self, x0, y0, x1, y1, text, command, bgC="", activeC="", 
                textC="#143936", activeTextC="#28DBBB", disabled=False, disabledBgC="#DCEAEA", disabledTextC="#91A3A3"):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.text = text
        self.command = command
        self.disabled = disabled
        self.hover = False

        # colors
        self.bgC = bgC
        self.activeC = activeC
        self.textC = textC
        self.activeTextC = activeTextC
        self.disabledBgC = disabledBgC
        self.disabledTextC = disabledTextC

    def __repr__(self):
        return f'Bbutton(x0={self.x0}, y0={self.y0}, x1={self.x1}, y1={self.y1}, text={self.text}, command={self.command})'

    def disable(self):
        self.disabled = True

    def enable(self):
        self.disabled = False

    def setCommand(self, command): # where command is a function
        self.command = command

    def onClick(self, app, event):
        x, y = event.x, event.y
        if not self.disabled:
            if x>=self.x0 and x<=self.x1 and y>=self.y0 and y<=self.y1:
                self.command(app)
                return True
        return False

    def onHover(self, event):
        x, y = event.x, event.y
        if not self.disabled:
            if x>=self.x0 and x<=self.x1 and y>=self.y0 and y<=self.y1:
                self.hover = True
            else:
                self.hover = False

    def drawButton(self, app, canvas):
        width, height = self.x1-self.x0, self.y1-self.y0
        font = "Open Sans", f"{int(height/2)}"
        if self.disabled:
            canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill=self.disabledBgC)
            canvas.create_text(self.x0+width/2, self.y0+height/2, text=self.text, font=font, fill=self.disabledTextC)
        elif self.hover:
            canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill=self.activeC)
            canvas.create_text(self.x0+width/2, self.y0+height/2, text=self.text, font=font, fill=self.activeTextC)
        else:
            canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill=self.bgC)
            canvas.create_text(self.x0+width/2, self.y0+height/2, text=self.text, font=font, fill=self.textC)

class PlanMeeting(Bbutton):
    def __init__(self, x0, y0, x1, y1, text, command):
        super().__init__(x0, y0, x1, y1, text, command, "#28DBBB", "#143936", "#143936", "#28DBBB")
            
    def __repr__(self):
        super().__repr__()

class Proceed(Bbutton):
    def __init__(self, x0, y0, x1, y1, text, command):
        super().__init__(x0, y0, x1, y1, text, command, "#28DBBB", "#143936", "#143936", "#28DBBB", disabled=True)

    def __repr__(self):
        super().__repr__()

    def arrowFloat(self):
        pass

class EventBox(Bbutton):
    def __init__(self, app, x0, y0, x1, y1, e_id, command, mine=False):
        self.event = e_id
        if mine==False:
            self.mine = e_id in app.currentUser.myEvents
        else:
            self.mine = mine
        super().__init__(x0, y0, x1, y1, app.events[e_id].name, command, bgC="",
            activeC="#DCEAEA", textC="#143936", activeTextC="#143936")

    def __repr__(self):
        return f'EventBox(x0={self.x0}, y0={self.y0}, x1={self.x1}, y1={self.y1}, e_id={self.event}, mine={self.mine}, command={self.command})'

    def onClick(self, app, event):
        x, y = event.x, event.y
        if not self.disabled:
            if x>=self.x0 and x<=self.x1 and y>=self.y0 and y<=self.y1:
                self.command(app, self.event)
                return True
        return False

    def drawButton(self, app, canvas):
        width, height = self.x1-self.x0, self.y1-self.y0
        font = "Avenir Next Medium", f"{int(height/2)}", "italic"
        smallFont = "Avenir Next Medium", f"{int(height/3)}"
        outlineC = "#143936"
        if self.disabled:
            canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill=self.disabledBgC, outline=outlineC)
            canvas.create_text(self.x0+width/16, self.y0+height/2, text=self.text, font=font, fill=self.disabledTextC, anchor=W)
            canvas.create_rectangle(self.x1-width/4, self.y0+5, self.x1-width/8, self.y1-5, fill=self.disabledTextC, outline=outlineC)
            canvas.create_text(self.x1-width*3/16, self.y0+height/2, text="GO", font=smallFont, fill=self.disabledBgC)
        elif self.hover:
            if not self.mine:
                canvas.create_rectangle(self.x0-3, self.y0-3, self.x1+3, self.y1+3, fill="#9FF8E2")
            canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill=self.activeC, outline=outlineC)
            canvas.create_text(self.x0+width/16, self.y0+height/2, text=self.text, font=font, fill=self.activeTextC, anchor=W)
            canvas.create_rectangle(self.x1-width/4, self.y0+5, self.x1-width/8, self.y1-5, fill="#143936", outline=outlineC)
            canvas.create_text(self.x1-width*3/16, self.y0+height/2, text="GO", font=smallFont, fill="#DCEAEA")
        else:
            if not self.mine:
                canvas.create_rectangle(self.x0-3, self.y0-3, self.x1+3, self.y1+3, fill="#9FF8E2")
            canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill=self.bgC, outline=outlineC)
            canvas.create_text(self.x0+width/16, self.y0+height/2, text=self.text, font=font, fill=self.textC, anchor=W)
            canvas.create_rectangle(self.x1-width/4, self.y0+5, self.x1-width/8, self.y1-5, fill="#143936", outline=outlineC)
            canvas.create_text(self.x1-width*3/16, self.y0+height/2, text="GO", font=smallFont, fill="#DCEAEA")