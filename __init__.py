#################################################
# __init__.py
#
# Your name: Yee Kit Chan
# Your andrew id: yeekitc
#################################################

import math, os, copy, decimal, datetime
from cmu_112_graphics import *
import module_manager
module_manager.review()

#################################################
# Splash Screen
#################################################

def splashScreenMode_appAttributes(app):
    app.welcText = 'w e l c o m e   t o   s e e_y o u_s o o n'
    app.welcInd = 0
    app.welcArrow = app.scaleImage(app.loadImage('rightArrow.png'), 1/3)
    app.arrWidth, app.arrHeight = app.welcArrow.size
    app.slide = False
    app.slideX0 = 0
    app.slideX = 0
    app.slide2X = 0
    app.splashTimer = 0
    app.timerDelay = 1

def splashScreenMode_redrawAll(app, canvas):
    font = 'Open Sans', '40'
    canvas.create_rectangle(0, 0, app.width, app.height, fill=app.bgC)
    canvas.create_text(app.width/2, app.height/2-40, 
        text=app.welcText[:app.welcInd+1], font=font, fill=app.textC)
    if app.welcInd+1 == len(app.welcText):
        # https://icons8.com/icon/39969/right-arrow
        canvas.create_image(app.width/2-app.arrWidth/2, app.height/2+40, 
                            image=ImageTk.PhotoImage(app.welcArrow))
    if app.slide:
        canvas.create_rectangle(0, 0, app.slide2X, app.height, fill=app.bgC)
        canvas.create_rectangle(app.slideX0, 0, app.slideX, app.height, fill=app.textC)
        
def splashScreenMode_timerFired(app):
    app.splashTimer += 1
    if app.welcInd+1 != len(app.welcText) and app.splashTimer%10 == 0:
        app.welcInd += 1
    elif app.slide:
        if app.slideX != app.width:
            app.slideX += 5
            app.slide2X += 5
        elif app.slideX0 != app.width:
            app.slideX0 += 5
        else:
            app.mode = "landingMode"

def splashScreenMode_mousePressed(app, event):
    if app.welcInd+1 == len(app.welcText):
        app.slide = True

def splashScreenMode_keyPressed(app, event):
    if app.welcInd+1 == len(app.welcText):
        app.slide = True

#################################################
# Landing Page
#################################################

def landingMode_appAttributes(app):
    pass

def landingMode_redrawAll(app, canvas):
    pass

##########################################
# Sign Up Page
##########################################

def signUpMode_appAttributes(app):
    pass

def signUpMode_redrawAll(app, canvas):
    pass

##########################################
# Sign In Page
##########################################

def signInMode_appAttributes(app):
    pass

def signInMode_redrawAll(app, canvas):
    pass

##########################################
# Event Availability Page (Attendee)
##########################################

def eventAvailMode_appAttributes(app):
    app.availGradient = ["#DCEAEA", "#9FF8E2", "#64EACF", "#28DBBB",
                        "#20B799", "#179376", "#137361", "#0F524C"]

def eventAvailMode_redrawAll(app, canvas):
    pass

def eventAvailMode_mousePressed(app, event):
    pass

def eventAvailMode_mouseReleased(app, event):
    pass

def eventAvailMode_mouseMoved(app, event):
    pass

def eventAvailMode_mouseDragged(app, event):
    pass

##########################################
# Creating Event Page
##########################################

def createEventMode_appAttributes(app):
    pass

def createEventMode_redrawAll(app, canvas):
    pass

##########################################
# Main App
##########################################

def appStarted(app):
    app.mode = 'splashScreenMode'
    app.score = 0
    app.timerDelay = 50
    # app.makeAnMVCViolation = False

    # colors
    app.bgC = "#FFFFFF"
    app.textC = "#143936"
    app.accentC = "#20B799"

    splashScreenMode_appAttributes(app)
    landingMode_appAttributes(app)
    signUpMode_appAttributes(app)
    signInMode_appAttributes(app)
    eventAvailMode_appAttributes(app)
    createEventMode_appAttributes(app)

runApp(width=1000, height=750)