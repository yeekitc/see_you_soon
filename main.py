#################################################
# __init__.py
#
# Your name: Yee Kit Chan
# Your andrew id: yeekitc
#################################################

import math, os, copy, decimal, datetime, random
from cmu_112_graphics import *
from button import *
from textBox import *
import module_manager
module_manager.review()

#################################################
# Splash Screen
#################################################

def splashScreenMode_appAttributes(app):
    app.welcText = 'w e l c o m e   t o   s e e_y o u_s o o n'
    app.welcInd = 0
    app.arrY = app.height/2+40
    app.arrDir = 1
    app.welcArrow = app.scaleImage(app.loadImage('rightArrow.png'), 1/3)
    app.arrWidth, app.arrHeight = app.welcArrow.size
    app.slide = False
    app.slideX0 = 0
    app.slideX = 0
    app.slide2X = 0
    app.splashTimer = 0

def splashScreenMode_redrawAll(app, canvas):
    font = 'Open Sans', '40'
    canvas.create_rectangle(0, 0, app.width, app.height, fill=app.bgC)
    canvas.create_text(app.width/2, app.height/2-40, 
        text=app.welcText[:app.welcInd+1], font=font, fill=app.textC)
    if app.welcInd+1 == len(app.welcText):
        # https://icons8.com/icon/39969/right-arrow
        canvas.create_image(app.width/2-app.arrWidth/2, app.arrY, 
                            image=ImageTk.PhotoImage(app.welcArrow))
    if app.slide:
        canvas.create_rectangle(0, 0, app.slide2X, app.height, fill=app.bgC)
        canvas.create_rectangle(app.slideX0, 0, app.slideX, app.height, fill=app.textC)
        
def splashScreenMode_timerFired(app):
    app.splashTimer += 1
    if app.splashTimer%6 == 0:
        if app.arrY <= app.height/2+20 or app.arrY > app.height/2+40:
            app.arrDir *= -1
        app.arrY -= 1*app.arrDir
    if app.welcInd+1 != len(app.welcText) and app.splashTimer%8 == 0:
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
    # app.matrixIm = app.scaleImage(app.loadImage('matrixPlaceholder.png'), 1)
    # app.matrixImWidth, app.matrixImHeight = app.matrixIm.size
    setMatrixCoords(app, app.width*13/24, app.navH+app.height*1/24, 
                 app.width, app.navH+app.height*21/24)
    app.landingMatrix = [[""]*app.cols for r in range(app.rows)]
    for r in range(app.rows):
        for c in range(app.cols):
            app.landingMatrix[r][c] = app.availGradient[random.randint(0,7)]
    app.meet2 = PlanMeeting(app.width/14, app.height/2+100, app.width*3/14, app.height/2+140, "Plan Meeting", meetMode)

def landingMode_sizeChanged(app):
    sizeChanged(app)

def landingMode_mouseMoved(app, event):
    app.meet2.onHover(event)
    hoverNav(app, event)

def landingMode_mousePressed(app, event):
    app.meet2.onClick(app, event)
    clickNav(app, event)

def landingMode_redrawAll(app, canvas):
    font = "Open Sans", f"{int(app.width/60)}"    
    drawNav(app, canvas)
    canvas.create_text(app.width/14, app.height/2-20, text="Welcome to see_you_soon!", 
                    font=app.titleFont, fill=app.textC, anchor=W)
    canvas.create_text(app.width/14, app.height/2+30, text="lorem ipsum text which will be a succinct description of the app and its function", 
                    font=font, fill=app.textC, width=app.width*10/24, anchor=NW)
    # canvas.create_image(app.width*23/24-app.matrixImWidth/2, (app.height-app.navH)/2+app.navH, 
    #                         image=ImageTk.PhotoImage(app.matrixIm))
    drawMatrix(app, canvas, app.landingMatrix)
    app.meet2.drawButton(app, canvas)

##########################################
# Sign Up Page
##########################################
# remember to change signedIn var
def signUpMode_appAttributes(app):
    app.signUpUserBox = TextBox(app.width/2-200, app.height*39/128, app.width/2+200, app.height*45/128)
    app.signUpUserBox.setBgText("Enter your username/email")
    app.signUpPWBox = TextBox(app.width/2-200, app.height*57/128, app.width/2+200, app.height*63/128, hidden=True)
    app.signUpPWBox.setBgText("Select a password")
    app.signUpConfirmBox = TextBox(app.width/2-200, app.height*75/128, app.width/2+200, app.height*81/128, hidden=True)
    app.signUpConfirmBox.setBgText("Confirm your password")
    app.signUpTimer = 0

    app.signUpPWsMatch = False
    app.signUpDone = Proceed(app.width/2-75, app.height*93/128, app.width/2+75, app.height*99/128, "-->", setSignedIn)

    app.haveAcc = Bbutton(app.width/2-125, app.height*105/128, app.width/2+125, app.height*111/128, 
        "have an account? sign in", signInMode)

def signUpMode_timerFired(app):
    app.signUpTimer += 1
    if app.signUpTimer%20 == 0:
        app.signUpUserBox.cursorBlink()
        app.signUpPWBox.cursorBlink()
        app.signUpConfirmBox.cursorBlink()
    if app.signUpPWBox.inText == app.signUpConfirmBox.inText:
        app.signUpPWsMatch = True
    else:
        app.signUpPWsMatch = False
    if (app.signUpUserBox.inText != "" and app.signUpPWBox.inText != "" and app.signUpConfirmBox != ""
        and app.signUpPWsMatch):
        app.signUpDone.disabled = False

def signUpMode_mouseMoved(app, event):
    hoverNav(app, event)
    app.signUpUserBox.onHover(event)
    app.signUpPWBox.onHover(event)
    app.signUpConfirmBox.onHover(event)
    app.signUpDone.onHover(event)
    app.haveAcc.onHover(event)

def signUpMode_mousePressed(app, event):
    clickNav(app, event)
    app.signUpUserBox.onClick(app, event)
    app.signUpPWBox.onClick(app, event)
    app.signUpConfirmBox.onClick(app, event)
    if app.signUpDone.onClick(app, event):
        # save inputs into accounts text file

        pass
    app.haveAcc.onClick(app, event)

def signUpMode_keyPressed(app, event):
    app.signUpUserBox.keysIn(event)
    app.signUpPWBox.keysIn(event)
    app.signUpConfirmBox.keysIn(event)

def signUpMode_sizeChanged(app):
    sizeChanged(app)

def signUpMode_redrawAll(app, canvas):
    drawNav(app, canvas)
    canvas.create_text(app.width/2, app.height*27/128, text="SIGN UP", font=app.titleFont, fill=app.textC)
    app.signUpUserBox.drawTextBox(app, canvas)
    app.signUpPWBox.drawTextBox(app, canvas)
    app.signUpConfirmBox.drawTextBox(app, canvas)
    app.signUpDone.drawButton(app, canvas)
    if not app.signUpPWsMatch and app.signUpUserBox.inText != "" and app.signUpPWBox.inText != "":
        canvas.create_text(app.width/2, app.height*89/128, text="*Please make sure your password confirmation matches!", 
            font=app.font, fill=app.nopeC)
    app.haveAcc.drawButton(app, canvas)

##########################################
# Sign In Page
##########################################
# remember to change signedIn var
def signInMode_appAttributes(app):
    app.signInUserBox = TextBox(app.width/2-200, app.height*39/128, app.width/2+200, app.height*45/128)
    app.signInUserBox.setBgText("Enter your username/email")
    app.signInPWBox = TextBox(app.width/2-200, app.height*57/128, app.width/2+200, app.height*63/128, hidden=True)
    app.signInPWBox.setBgText("Select a password")
    app.signInTimer = 0

    app.validUser = False
    app.signInDone = Proceed(app.width/2-75, app.height*75/128, app.width/2+75, app.height*81/128, "-->", setSignedIn)

    app.noAcc = Bbutton(app.width/2-125, app.height*87/128, app.width/2+125, app.height*93/128, 
        "don't have an account? sign up", signUpMode)

def signInMode_timerFired(app):
    app.signInTimer += 1
    if app.signInTimer%20 == 0:
        app.signInUserBox.cursorBlink()
        app.signInPWBox.cursorBlink()

    # if userVal(), app.validUser = True, else False
        
    if (app.signInUserBox.inText != "" and app.signInPWBox.inText != ""
        and app.validUser):
        app.signInDone.disabled = False

def userVal(user, pw):
    # returns true if valid user account info
    pass

def signInMode_sizeChanged(app):
    sizeChanged(app)

def signInMode_mouseMoved(app, event):
    hoverNav(app, event)
    app.signInUserBox.onHover(event)
    app.signInPWBox.onHover(event)
    app.signInDone.onHover(event)
    app.noAcc.onHover(event)

def signInMode_mousePressed(app, event):
    clickNav(app, event)
    app.signInUserBox.onClick(app, event)
    app.signInPWBox.onClick(app, event)
    if app.signInDone.onClick(app, event):
        # set the user to the entered user
        pass
    app.noAcc.onClick(app, event)

def signInMode_keyPressed(app, event):
    app.signInUserBox.keysIn(event)
    app.signInPWBox.keysIn(event)

def signInMode_redrawAll(app, canvas):
    drawNav(app, canvas)
    canvas.create_text(app.width/2, app.height*27/128, text="SIGN IN", font=app.titleFont, fill=app.textC)
    app.signInUserBox.drawTextBox(app, canvas)
    app.signInPWBox.drawTextBox(app, canvas)
    app.signInDone.drawButton(app, canvas)
    if not app.validUser and app.signInUserBox.inText != "" and app.signInPWBox.inText != "":
        canvas.create_text(app.width/2, app.height*69/128, text="*User not found!", font=app.font, fill=app.nopeC)
    app.noAcc.drawButton(app, canvas)

##########################################
# Event Availability Page (Attendee)
##########################################

def eventAvailMode_appAttributes(app):
    pass

def eventAvailMode_redrawAll(app, canvas):
    drawNav(app, canvas)

def eventAvailMode_sizeChanged(app):
    sizeChanged(app)

def eventAvailMode_mousePressed(app, event):
    clickNav(app, event)

def eventAvailMode_mouseReleased(app, event):
    pass

def eventAvailMode_mouseMoved(app, event):
    hoverNav(app, event)

def eventAvailMode_mouseDragged(app, event):
    pass

##########################################
# Creating Event Page
##########################################

def createEventMode_appAttributes(app):
    pass

def createEventMode_mouseMoved(app, event):
    hoverNav(app, event)

def createEventMode_mousePressed(app, event):
    clickNav(app, event)
    print(event.x, event.y)

def createEventMode_redrawAll(app, canvas):
    drawNav(app, canvas)

def createEventMode_sizeChanged(app):
    sizeChanged(app)

##########################################
# User Dashboard
##########################################

def dashboardMode_appAttributes(app):
    pass

def dashboardMode_mouseMoved(app, event):
    hoverNav(app, event)

def dashboardMode_mousePressed(app, event):
    clickNav(app, event)

def dashboardMode_redrawAll(app, canvas):
    drawNav(app, canvas)

def dashboardMode_sizeChanged(app):
    sizeChanged(app)

##########################################
# Main App
##########################################

def appStarted(app):
    # read data from file ---- put somewhere

    app.titleFont = "Open Sans", f"{int(app.width/30)}"
    app.font = "Open Sans", f"{int(app.width/60)}"
    app.mode = 'signUpMode'
    app.timerDelay = 5
    # app.makeAnMVCViolation = False
    app.signedIn = False
    app.user = ""
    app.navH = app.height/10

    # colors
    app.bgC = "#FFFFFF"
    app.textC = "#143936"
    app.accentC = "#20B799"
    app.emptyC = "#DCEAEA"
    app.availGradient = ["#DCEAEA", "#9FF8E2", "#64EACF", "#28DBBB",
                        "#20B799", "#179376", "#137361", "#0F524C"]
    app.nopeC = "#FA8072"

    # logo (designed via Canva)
    app.logo = app.scaleImage(app.loadImage('logo.png'), 1/3)
    app.logoWidth, app.logoHeight = app.logo.size

    # availability matrix
    app.currentEvent = ""
    app.rows = 18               # default: 9-5
    app.cols = 7                # default: 1 week
    app.marginX = 5             # horizontal margin around grid
    app.marginY = 5             # vertical margin around grid 
    app.selection = (-1, -1)    # (row, col) of selection, (-1, -1) for none
    app.matrixX0 = 0
    app.matrixY0 = 0
    app.matrixX1 = 0
    app.matrixY1 = 0
    app.days = ["Sun", "Mon", "Tues", "Weds", "Thurs", "Fri", "Sat"]
    app.times = [9, 10, 11, 12, 13, 14, 15, 16, 17]

    # buttons
    app.navMeet = PlanMeeting(app.width*23/28, app.navH/2-20, app.width*27/28, app.navH/2+20, "Plan Meeting", meetMode)
    app.navSignIn = Bbutton(app.width*19/28, app.navH/2-20, app.width*23/28, app.navH/2+20, "Sign In", signInMode)
    app.navDashboard = Bbutton(app.width*19/28, app.navH/2-20, app.width*23/28, app.navH/2+20, "Dashboard", dashMode)

    splashScreenMode_appAttributes(app)
    landingMode_appAttributes(app)
    signUpMode_appAttributes(app)
    signInMode_appAttributes(app)
    eventAvailMode_appAttributes(app)
    createEventMode_appAttributes(app)

# https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

# https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

# upon pressing the Plan New Meeting Button
def meetMode(app):
    if app.signedIn:
        app.mode = "createEventMode"
    else:
        app.mode = "signInMode"

# upon pressing "Sign In"
def signInMode(app):
    if app.signedIn:
        dashMode(app)
    else:
        app.mode = "signInMode"

# upon pressing "Sign Up"
def signUpMode(app):
    app.mode = "signUpMode"

# go to the user's dashboard"
def dashMode(app):
    if not app.signedIn:
        app.mode = "signInMode"
    else:
        app.mode = "dashboardMode"

# go to the landing page
def landingPgMode(app):
    app.mode = "landingMode"

# go to the event availability page
def eventAvailMode(app):
    if app.signedIn:
        app.mode = "eventAvailMode"
    else:
        app.mode = "signInMode"

# the user is signed in
def setSignedIn(app):
    app.signedIn = True
    app.mode = "dashboardMode"

# the user is signed out
def setSignedOut(app):
    app.signedIn = False

# sets the current event
def setCurrentEvent(app, Event):
    app.currentEvent = Event

# sets the dimensions of the availability matrix
def setMatrixCoords(app, x0, y0, x1, y1):
    app.matrixX0 = x0
    app.matrixY0 = y0
    app.matrixX1 = x1
    app.matrixY1 = y1
    app.marginX = (x1-x0)/app.cols
    app.marginY = (y1-y0)/app.rows

# sets the rows and cols of the availability matrix
def setMatrixDims(app, rows, cols):
    app.rows = rows
    app.cols = cols
    app.marginX = (app.matrixX1-app.matrixX0)/cols
    app.marginY = (app.matrixY1-app.matrixY0)/rows

# making the app layout responsive
def sizeChanged(app):
    app.navH = app.height/10
    app.font = "Open Sans", f"{int(app.width/60)}"
    setMatrixCoords(app, app.width*13/24, app.navH+app.height*1/24, 
                 app.width, app.navH+app.height*21/24)

# modified from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
def pointInGrid(app, x, y):
    # return True if (x, y) is inside the grid defined by app.
    return ((app.marginX+app.matrixX0 <= x <= app.matrixX1-app.marginX) and
            (app.marginY+app.matrixY0 <= y <= app.matrixY1-app.marginY))

# modified from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
def getCell(app, x, y):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(app, x, y)):
        return (-1, -1)
    gridWidth  = (app.matrixX1-app.matrixX0) - 2*app.marginX
    gridHeight = (app.matrixY1-app.matrixY0) - 2*app.marginY
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows

    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, app.margin,
    # cellWidth or cellHeight are floats, // would still produce floats.
    row = int((y - app.marginY - app.matrixY0) / cellHeight)
    col = int((x - app.marginX - app.matrixX0) / cellWidth)

    return (row, col)

# when hovering over buttons in the nav bar
def hoverNav(app, event):
    x, y = event.x, event.y
    app.navMeet.onHover(event)
    if app.signedIn:
        app.navDashboard.onHover(event)
    else:
        app.navSignIn.onHover(event)

# when clicking buttons in the nav bar
def clickNav(app, event):
    x, y = event.x, event.y
    if x>=20 and x<=(app.navH-40)*3+20 and y>=0 and y<=app.navH:
        landingPgMode(app)
    app.navMeet.onClick(app, event)
    if app.signedIn:
        app.navDashboard.onClick(app, event)
    else:
        app.navSignIn.onClick(app, event)

# draws the nav bar of the app
def drawNav(app, canvas):
    font = "Open Sans", f"{int(app.navH*7/24)}"
    canvas.create_rectangle(0, 0, app.width, app.navH, fill=app.emptyC)
    # canvas.create_image(20+app.logoWidth/2, 20+app.logoHeight/2, image=ImageTk.PhotoImage(app.logo))
    drawLogo(app, canvas, 20, 20, (app.navH-40)*3+20)
    if app.signedIn:
        app.navDashboard.drawButton(app, canvas)
    else:  
        app.navSignIn.drawButton(app, canvas)
    app.navMeet.drawButton(app, canvas)

# draws the SEE_YOU_SOON logo
def drawLogo(app, canvas, x0, y0, x1):
    y1 = y0+(x1-x0)/3
    width, height = x1-x0, y1-y0
    font = "Open Sans", f"{int(height*5/16)}"
    canvas.create_rectangle(x0, y0, x1, y1, fill=app.accentC)
    canvas.create_rectangle(x0+width/35, y0+height*3/35, x1-width/35, y1-height*3/35, fill=app.emptyC)
    canvas.create_rectangle(x0+width*2/35, y0+height*6/35, x1-width*2/35, y1-height*6/35, fill=app.textC)
    canvas.create_text(x0+width/2, y0+height/2, text="SEE_YOU_SOON", font=font, fill=app.bgC)

# modified from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
def getCellBounds(app, row, col):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = (app.matrixX1-app.matrixX0) - 2*app.marginX
    gridHeight = (app.matrixY1-app.matrixY0) - 2*app.marginY
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.matrixX0 + app.marginX + col * cellWidth
    x1 = app.matrixX0 + app.marginX + (col+1) * cellWidth
    y0 = app.matrixY0 + app.marginY + row * cellHeight
    y1 = app.matrixY0 + app.marginY + (row+1) * cellHeight
    return (x0, y0, x1, y1)

# draws matrix based on possible days (currently default 7) & times (default 9-5)
def drawMatrix(app, canvas, matrix):
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#exampleGrids
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            fill = matrix[row][col]
            canvas.create_rectangle(x0, y0, x1, y1, fill=fill)
    drawMatrixLabels(app, canvas)

# draws labels on the horizontal & vertical axes of the availability matrix
def drawMatrixLabels(app, canvas):
    gridWidth  = (app.matrixX1-app.matrixX0) - 2*app.marginX
    gridHeight = (app.matrixY1-app.matrixY0) - 2*app.marginY
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    font = "Open Sans", f"{int(cellHeight/2)}", "bold"
    for day in range(len(app.days)):
        canvas.create_text(app.marginX+app.matrixX0+cellWidth/2+cellWidth*day, app.matrixY0+cellHeight/2, 
                        text=app.days[day], fill=app.textC, font=font)
    for time in range(len(app.times)):
        meridiem = ""
        text = ""
        if app.times[time] > 12:
            meridiem = " PM"
        else:
            meridiem = " AM"
        if app.times[time]%12 == 0:
            text = "12" + meridiem
        else:
            text = f"{app.times[time]%12}" + meridiem
        canvas.create_text(app.matrixX0+cellWidth/2, app.marginY+app.matrixY0+cellHeight*(2*time+1),
                        text=text, fill=app.textC, font=font)

def appStopped(app):
    # save data to file
    pass


runApp(width=1250, height=750)