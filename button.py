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
    def __init__(self, app, x0, y0, x1, y1, Event, command):
        self.event = Event
        self.responded = Event in app.currentUser.myEvents
        super().__init__(x0, y0, x1, y1, Event.title, command)

    def __repr__(self):
        super().__repr__()

    def drawButton(self, app, canvas):
        if self.responded:
            self.bgC = "#9FF8E2"
            self.activeC = "#0F524C"
            self.textC = "#143936"
            self.activeTextC = "#FFFFFF"
        else:
            self.bgC = ""
            self.activeC = "#DCEAEA"
            self.textC = "#143936"
            self.activeTextC = "#143936"