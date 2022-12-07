#################################################
# main.py
#
# Your name: Yee Kit Chan
# Your andrew id: yeekitc
#################################################

import random, ast
from cmu_112_graphics import *
from button import *
from textBox import *
from matrix import *
from user import *
from event import *
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
    # https://icons8.com/icon/39969/right-arrow
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
        if app.slideX <= app.width:
            app.slideX += 10
            app.slide2X += 10
        elif app.slideX0 <= app.width:
            app.slideX0 += 10
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
    app.landingMatrix = Matrix(app.width*13/24, app.navH+app.height*1/24, 
                 app.width, app.navH+app.height*21/24)

    for r in range(app.rows):
        for c in range(app.cols):
            app.landingMatrix.matrix[r][c] = random.randint(0,7)
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
    canvas.create_text(app.width/14, app.height/2+30, text="gather your guests' availabilities and find the best time to meet, painlessly", 
                    font=font, fill=app.textC, width=app.width*10/24, anchor=NW)

    app.landingMatrix.drawMatrix(app, canvas)

    app.meet2.drawButton(app, canvas)

##########################################
# Sign Up Page
##########################################
def signUpMode_appAttributes(app):
    app.signUpUserBox = TextBox(app.width/2-200, app.height*39/128, app.width/2+200, app.height*45/128)
    app.signUpUserBox.setBgText("Enter your username/email")
    app.signUpPWBox = TextBox(app.width/2-200, app.height*57/128, app.width/2+200, app.height*63/128, hidden=True)
    app.signUpPWBox.setBgText("Select a password")
    app.signUpConfirmBox = TextBox(app.width/2-200, app.height*75/128, app.width/2+200, app.height*81/128, hidden=True)
    app.signUpConfirmBox.setBgText("Confirm your password")
    app.signUpTimer = 0

    app.signUpExists = False
    app.signUpPWsMatch = False
    app.signUpDone = Proceed(app.width/2-75, app.height*93/128, app.width/2+75, app.height*99/128, "-->", signInMode)

    app.haveAcc = Bbutton(app.width/2-125, app.height*105/128, app.width/2+125, app.height*111/128, 
        "have an account? sign in", signInMode)

def signUpMode_timerFired(app):
    app.signUpTimer += 1
    user = app.signUpUserBox.inText
    pw = app.signUpPWBox.inText
    confirm = app.signUpConfirmBox.inText
    if app.signUpTimer%20 == 0:
        app.signUpUserBox.cursorBlink()
        app.signUpPWBox.cursorBlink()
        app.signUpConfirmBox.cursorBlink()
    if user != "" and pw != "" and confirm != "":
        if pw == confirm:
            app.signUpPWsMatch = True
        else:
            app.signUpPWsMatch = False
        
        if user in app.accounts:
            app.signUpExists = True
        else:
            app.signUpExists = False

        if app.signUpPWsMatch and not app.signUpExists:
            app.signUpDone.disabled = False
        else:
            app.signUpDone.disabled = True

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
        user = app.signUpUserBox.inText
        pw = app.signUpPWBox.inText
        app.accounts[user] = pw
        # save inputs into accounts text file
        writeFile(user+"_invited_events.g", "[]")
        writeFile(user+"_hosted_events.g", "[]")
        writeFile('accounts.txt', repr(app.accounts))

        # clear all app.___.inTexts
        signUpMode_appAttributes(app)
    app.haveAcc.onClick(app, event)

def signUpMode_keyPressed(app, event):
    app.signUpUserBox.keysIn(event)
    app.signUpPWBox.keysIn(event)
    app.signUpConfirmBox.keysIn(event)

def signUpMode_sizeChanged(app):
    sizeChanged(app)

def signUpMode_redrawAll(app, canvas):
    user = app.signUpUserBox.inText
    pw = app.signUpPWBox.inText
    confirm = app.signUpConfirmBox.inText

    drawNav(app, canvas)
    canvas.create_text(app.width/2, app.height*27/128, text="SIGN UP", font=app.titleFont, fill=app.textC)
    app.signUpUserBox.drawTextBox(app, canvas)
    app.signUpPWBox.drawTextBox(app, canvas)
    app.signUpConfirmBox.drawTextBox(app, canvas)
    app.signUpDone.drawButton(app, canvas)
    if (not app.signUpPWsMatch) and user != "" and pw != "" and confirm != "":
        canvas.create_text(app.width/2, app.height*89/128, text="*Please make sure your password confirmation matches!", 
            font=app.font, fill=app.nopeC)
    elif app.signUpExists:
        canvas.create_text(app.width/2, app.height*89/128, text="*User already exists in database", 
            font=app.font, fill=app.nopeC)
    app.haveAcc.drawButton(app, canvas)

##########################################
# Sign In Page
##########################################
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
    user = app.signInUserBox.inText
    pw = app.signInPWBox.inText
    app.signInTimer += 1

    if app.signInTimer%20 == 0:
        app.signInUserBox.cursorBlink()
        app.signInPWBox.cursorBlink()

    if userVal(app, user, pw):
        app.validUser = True
    else:
        app.validUser = False
        
    if (user != "" and pw != "" and app.validUser):
        app.signInDone.disabled = False
    else:
        app.signInDone.disabled = True

# returns true if valid user account info
def userVal(app, user, pw):
    if app.accounts.get(user) == pw:
        return True
    return False

def signInMode_sizeChanged(app):
    sizeChanged(app)

def signInMode_mouseMoved(app, event):
    hoverNav(app, event)
    app.signInUserBox.onHover(event)
    app.signInPWBox.onHover(event)
    app.signInDone.onHover(event)
    app.noAcc.onHover(event)

def signInMode_mousePressed(app, event):
    user = app.signInUserBox.inText
    clickNav(app, event)
    app.signInUserBox.onClick(app, event)
    app.signInPWBox.onClick(app, event)
    if app.signInDone.onClick(app, event):
        app.user = user
        invitede = ast.literal_eval(readFile(user + "_invited_events.g"))
        hostede = ast.literal_eval(readFile(user + "_hosted_events.g"))
        u = User(user, "(encrypted)", invitedEvents=invitede, myEvents=hostede)
        app.currentUser = u
        dashboardMode_updateEvents(app)
        app.mode = "dashboardMode"
    app.noAcc.onClick(app, event)

def signInMode_keyPressed(app, event):
    app.signInUserBox.keysIn(event)
    app.signInPWBox.keysIn(event)

def signInMode_redrawAll(app, canvas):
    user = app.signInUserBox.inText
    pw = app.signInPWBox.inText
    drawNav(app, canvas)
    canvas.create_text(app.width/2, app.height*27/128, text="SIGN IN", font=app.titleFont, fill=app.textC)
    app.signInUserBox.drawTextBox(app, canvas)
    app.signInPWBox.drawTextBox(app, canvas)
    app.signInDone.drawButton(app, canvas)
    if not app.validUser and user != "" and pw != "":
        canvas.create_text(app.width/2, app.height*69/128, text="*User not found!", font=app.font, fill=app.nopeC)
    app.noAcc.drawButton(app, canvas)

##########################################
# Creating Event Page
##########################################

def createEventMode_appAttributes(app):
    app.eEarliestAMPM = "AM"
    app.eLatestAMPM = "AM"
    app.createEventTimer = 0
    app.eEarlyTime = False
    app.eLateTime = False
    app.eDaysValid = False
    app.eInviteValid = False

    app.eName = TextBox(app.width/2-100, app.navH+150, app.width/2+100, app.navH+180)
    app.eName.setBgText("set event name")
    app.eDays = TextBox(app.width/2-100, app.navH+220, app.width/2+100, app.navH+250)
    app.eDays.setBgText("enter weekdays")
    app.eEarliest = TextBox(app.width/2-300, app.navH+290, app.width/2-120, app.navH+320)
    app.eEarliest.setBgText("earliest possible time")
    app.eEarlyAM = Bbutton(app.width/2-100, app.navH+290, app.width/2-70, app.navH+320, "AM", setEarlyAM, 
                    bgC="#28DBBB", activeC="#143936", textC="#143936", activeTextC="#28DBBB")
    app.eEarlyPM = Bbutton(app.width/2-50, app.navH+290, app.width/2-20, app.navH+320, "PM", setEarlyPM, 
                    activeC="#28DBBB", activeTextC="#143936")
    app.eLatest = TextBox(app.width/2+20, app.navH+290, app.width/2+200, app.navH+320)
    app.eLateAM = Bbutton(app.width/2+220, app.navH+290, app.width/2+250, app.navH+320, "AM", setLateAM, 
                    bgC="#28DBBB", activeC="#143936", textC="#143936", activeTextC="#28DBBB")
    app.eLatePM = Bbutton(app.width/2+270, app.navH+290, app.width/2+300, app.navH+320, "PM", setLatePM, 
                    activeC="#28DBBB", activeTextC="#143936")
    app.eLatest.setBgText("latest possible time")
    app.eInvite = TextBox(app.width/2-200, app.navH+360, app.width/2+200, app.navH+390)
    app.eInvite.setBgText("search for users to invite (directory below)")

    app.eCreate = Proceed(app.width/2+250, app.navH+360, app.width/2+300, app.navH+390, "-->", dashMode)
    app.eCreated = False

def setEarlyAM(app):
    # set PM to off color, set eEarliestAMPM to AM
    app.eEarliestAMPM = "AM"

    app.eEarlyAM.bgC = "#28DBBB"
    app.eEarlyAM.activeC = "#143936"
    app.eEarlyAM.textC = "#143936"
    app.eEarlyAM.activeTextC = "#28DBBB"

    app.eEarlyPM.bgC = ""
    app.eEarlyPM.activeC = "#28DBBB"
    app.eEarlyPM.textC = "#143936"
    app.eEarlyPM.activeTextC = "#143936"

def setEarlyPM(app):
    # set AM to off color, set eEarliestAMPM to PM
    app.eEarliestAMPM = "PM"

    app.eEarlyAM.bgC = ""
    app.eEarlyAM.activeC = "#28DBBB"
    app.eEarlyAM.textC = "#143936"
    app.eEarlyAM.activeTextC = "#143936"

    app.eEarlyPM.bgC = "#28DBBB"
    app.eEarlyPM.activeC = "#143936"
    app.eEarlyPM.textC = "#143936"
    app.eEarlyPM.activeTextC = "#28DBBB"

def setLateAM(app):
    # set PM to off color, set eEarliestAMPM to AM
    app.eLatestAMPM = "AM"

    app.eLateAM.bgC = "#28DBBB"
    app.eLateAM.activeC = "#143936"
    app.eLateAM.textC = "#143936"
    app.eLateAM.activeTextC = "#28DBBB"

    app.eLatePM.bgC = ""
    app.eLatePM.activeC = "#28DBBB"
    app.eLatePM.textC = "#143936"
    app.eLatePM.activeTextC = "#143936"

def setLatePM(app):
    # set AM to off color, set eEarliestAMPM to PM
    app.eLatestAMPM = "PM"

    app.eLateAM.bgC = ""
    app.eLateAM.activeC = "#28DBBB"
    app.eLateAM.textC = "#143936"
    app.eLateAM.activeTextC = "#143936"

    app.eLatePM.bgC = "#28DBBB"
    app.eLatePM.activeC = "#143936"
    app.eLatePM.textC = "#143936"
    app.eLatePM.activeTextC = "#28DBBB"

def createEventMode_timerFired(app):
    eName = app.eName.inText
    eDays = app.eDays.inText
    eEarliest = app.eEarliest.inText
    eLatest = app.eLatest.inText
    eInvite = app.eInvite.inText
    app.createEventTimer += 1

    if app.createEventTimer%20 == 0:
        app.eName.cursorBlink()
        app.eDays.cursorBlink()
        app.eEarliest.cursorBlink()
        app.eLatest.cursorBlink()
        app.eInvite.cursorBlink()

    app.eDaysValid = weekdaysValid(eDays)
        
    if eEarliest.isdigit() and int(eEarliest)>=0 and int(eEarliest)<=12:
        app.eEarlyTime = True
    else:
        app.eEarlyTime = False
    if eLatest.isdigit() and int(eLatest)>=0 and int(eLatest)<=12:
        app.eLateTime = True
    else:
        app.eLateTime = False

    app.eInviteValid = userSearch(app, eInvite)

    if (eName!="" and eDays!="" and eEarliest!="" and eLatest!="" and eInvite!="" 
        and app.eEarlyTime and app.eLateTime and app.eDaysValid and app.eInviteValid):
        app.eCreate.disabled = False
    else:
        app.eCreate.disabled = True

def userSearch(app, users):
    for user in users.split(","):
        if user.strip().lower() not in app.accounts:
            return False
    return True

def weekdaysValid(days):
    weekdays = {"sun", "mon", "tues", "weds", "thurs", "fri", "sat",
                "sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"}
    for day in days.split(","):
        if day.strip().lower() not in weekdays:
            return False
    return True

def createEventMode_mouseMoved(app, event):
    hoverNav(app, event)
    app.eName.onHover(event)
    app.eDays.onHover(event)
    app.eEarliest.onHover(event)
    app.eLatest.onHover(event)
    app.eInvite.onHover(event)

    app.eEarlyAM.onHover(event)
    app.eEarlyPM.onHover(event)
    app.eLateAM.onHover(event)
    app.eLatePM.onHover(event)

def createEventMode_mousePressed(app, event):
    eName = app.eName.inText
    eDays = app.eDays.inText
    eEarliest = app.eEarliest.inText
    eLatest = app.eLatest.inText
    eInvite = app.eInvite.inText

    clickNav(app, event)
    app.eName.onClick(app, event)
    app.eDays.onClick(app, event)
    app.eEarliest.onClick(app, event)
    app.eLatest.onClick(app, event)
    app.eInvite.onClick(app, event)

    app.eEarlyAM.onClick(app, event)
    app.eEarlyPM.onClick(app, event)
    app.eLateAM.onClick(app, event)
    app.eLatePM.onClick(app, event)

    if app.eCreate.onClick(app, event):
        # make the weekdays into a processable list
        days = eDays
        dayList = []
        for day in days.split(","):
            day = day.strip().lower()
            dayList += [day]
        # make the times processable
        timeList = []
        early = int(eEarliest)
        late = int(eLatest)
        if app.eEarliestAMPM=="PM":
            early += 12
        if app.eLatestAMPM=="PM":
            late += 12
        for i in range(early, late+1):
            timeList += [i]
        # make the users into a processable list
        users = eInvite
        userList = [app.user]
        for user in users.split(","):
            user = user.strip().lower()
            if user != app.user:
                userList += [user]
        # save event
        id = addEvent(app, eName, dayList, timeList)
        for user in userList:
            if user == app.user:
                app.currentUser.invitedEvents += [id]
            userdata = ast.literal_eval(readFile(user+"_invited_events.g"))
            userdata += [id]
            # temporarily generate random priorities for heuristic algorithm
            randPriority = random.randint(0, 7)
            updateUserAvailMatrixGivenName(app, user, id, Matrix(app.width*2/24, app.navH+app.height*2/24, 
                 app.width*13/24, app.navH+app.height*22/24), randPriority)
            writeFile(user+"_invited_events.g", str(userdata))
        # update dashboard events
        dashboardMode_updateEvents(app)
        # clear all app.___.inTexts
        createEventMode_appAttributes(app)

def createEventMode_keyPressed(app, event):
    app.eName.keysIn(event)
    app.eDays.keysIn(event)
    app.eEarliest.keysIn(event)
    app.eLatest.keysIn(event)
    # if eEarliest/eLatest ends in PM, add 12
    app.eInvite.keysIn(event)

def createEventMode_redrawAll(app, canvas):
    eName = app.eName.inText
    eDays = app.eDays.inText
    eEarliest = app.eEarliest.inText
    eLatest = app.eLatest.inText
    eInvite = app.eInvite.inText
    uList = ""
    font = ("Open Sans", 16)

    drawNav(app, canvas)
    canvas.create_text(app.width/2, app.height*27/128, text="CREATE AN EVENT", font=app.titleFont, fill=app.textC)
    app.eName.drawTextBox(app, canvas)
    app.eDays.drawTextBox(app, canvas)
    if not app.eDaysValid and eDays!="":
        canvas.create_text(app.width/2, app.navH+260, text="*Invalid days!", 
            font=font, fill=app.nopeC)

    app.eEarliest.drawTextBox(app, canvas)
    app.eEarlyAM.drawButton(app, canvas)
    app.eEarlyPM.drawButton(app, canvas)
    if not app.eEarlyTime and eEarliest!="":
        canvas.create_text(app.width/2-210, app.navH+330, text="*Invalid time!", 
            font=font, fill=app.nopeC)

    app.eLatest.drawTextBox(app, canvas)
    app.eLateAM.drawButton(app, canvas)
    app.eLatePM.drawButton(app, canvas)
    if not app.eLateTime and eLatest!="":
        canvas.create_text(app.width/2+110, app.navH+330, text="*Invalid time!", 
            font=font, fill=app.nopeC)
    
    app.eInvite.drawTextBox(app, canvas)
    if not app.eInviteValid and eInvite!="":
        canvas.create_text(app.width/2, app.navH+400, text="*Last user not found!", 
            font=font, fill=app.nopeC)
    app.eCreate.drawButton(app, canvas)

    uListofLists = []
    uList = []
    alphaAccs = sorted(app.accounts)
    for user in range(len(alphaAccs)):
        if user%10==0:
            uListofLists += [uList]
            uList = []
        uList += [alphaAccs[user]]
    uListofLists += [uList]
    uListofLists = uListofLists[1:]

    printUList = ""
    userList = uListofLists[0]
    for i in range(len(userList)):
        printUList += userList[i]
        for uListI in range(1, len(uListofLists)):
            printUList += "\t"
            if i < len(uListofLists[uListI]):
                printUList += uListofLists[uListI][i]
        if i < len(userList)-1:
            printUList += "\n"

    canvas.create_text(app.width/2, app.navH+420, text=printUList, font=font, fill="#137361", anchor=N)

def createEventMode_sizeChanged(app):
    sizeChanged(app)

##########################################
# User Dashboard
##########################################

def dashboardMode_appAttributes(app):
    app.dashInvitedEs = []
    app.dashMyEs = []

def dashboardMode_updateEvents(app):
    setOfEs = set()
    for e in range(len(app.currentUser.myEvents)):
        app.dashMyEs += [EventBox(app, app.width*18/32, app.height*31/128+50*e, app.width*28/32, app.height*31/128+50*(e+1), app.currentUser.myEvents[e], eventAvailMode, mine=True)]
        setOfEs.add(app.currentUser.myEvents[e])
    e2 = 0
    while e2 in range(len(app.currentUser.invitedEvents)):
        if app.currentUser.invitedEvents[e2] in setOfEs:
            app.currentUser.invitedEvents.pop(e2)
        else:
            e2 += 1
    for e3 in range(len(app.currentUser.invitedEvents)):
        app.dashInvitedEs += [EventBox(app, app.width*4/32, app.height*31/128+50*e3, app.width*14/32, app.height*31/128+50*(e3+1), app.currentUser.invitedEvents[e3], eventAvailMode)]

def dashboardMode_mouseMoved(app, event):
    hoverNav(app, event)
    for eventBox in app.dashInvitedEs:
        eventBox.onHover(event)
    for eventBox in app.dashMyEs:
        eventBox.onHover(event)

def dashboardMode_mousePressed(app, event):
    clickNav(app, event)
    for eventBox in app.dashInvitedEs:
        eventBox.onClick(app, event)
    for eventBox in app.dashMyEs:
        eventBox.onClick(app, event)

def dashboardMode_redrawAll(app, canvas):
    drawNav(app, canvas)
    canvas.create_text(app.width*9/32, app.height*23/128, text="invites", font=app.titleFont, fill=app.textC)
    canvas.create_text(app.width*23/32, app.height*23/128, text="my events", font=app.titleFont, fill=app.textC)

    for eventBox in app.dashInvitedEs:
        eventBox.drawButton(app, canvas)
    for eventBox in app.dashMyEs:
        eventBox.drawButton(app, canvas)

def dashboardMode_sizeChanged(app):
    sizeChanged(app)

##########################################
# Event Availability Page (Attendee)
##########################################

def eventAvailMode_appAttributes(app):
    app.currentEventID = -1
    app.inputMatrix = Matrix(app.width*2/24, app.navH+app.height*2/24, 
                 app.width*13/24, app.navH+app.height*22/24)
    app.userPriority = -1
    app.eventMatrix = EventMatrix(app.width*13/24, app.navH+app.height*2/24, 
                 app.width, app.navH+app.height*22/24)
    app.enableRec = False
    app.recButton = Bbutton(app.width/2-10, app.navH+25, app.width/2+90, app.navH+55, "Recommend", toggleRecs)
    app.inputAppear = True
    app.usersAppear = False
    app.usersAvailable = []

def eventAvailMode_updateUserMatrix(app):
    _event = app.events[app.currentEventID]
    app.inputMatrix, app.userPriority = _event.usersAvail[app.user]

def eventAvailMode_updateEventMatrix(app):
    # aggregates the availabilities of the invited users
    _event = app.events[app.currentEventID]
    tempEMatrix = EventMatrix(app.width*13/24, app.navH+app.height*2/24, 
                 app.width, app.navH+app.height*22/24)
    for user in _event.usersAvail:
        avail, pri = _event.usersAvail[user]
        for r in range(len(avail.matrix)):
            for c in range(len(avail.matrix[0])):
                tempEMatrix.matrix[r][c] += avail.matrix[r][c]
    app.eventMatrix = tempEMatrix

def recommendTime(app):
    _event = app.events[app.currentEventID]
    myAvail, myPri = _event.usersAvail[app.user]
    rows, cols = len(myAvail.matrix), len(myAvail.matrix[0])
    priMatrix = [[0]*cols for r in range(rows)]
    for user in _event.usersAvail:
        avail, pri = _event.usersAvail[user]
        for r in range(len(avail.matrix)):
            for c in range(len(avail.matrix[0])):
                if avail.matrix[r][c] > 0:
                    priMatrix[r][c] += pri
    priMax = 0
    maxPriR = -1
    maxPriC = -1
    for r in range(len(priMatrix)):
        for c in range(len(priMatrix[0])):
            if priMatrix[r][c] >= priMax:
                priMax = priMatrix[r][c]
                maxPriR = r
                maxPriC = c
    return maxPriR, maxPriC

def usersAvailable(app, r, c):
    _event = app.events[app.currentEventID]
    usersAvailable = []
    for user in _event.usersAvail:
        avail, pri = _event.usersAvail[user]
        if avail.matrix[r][c] > 0:
            usersAvailable += [user]
    app.usersAvailable = usersAvailable    

def toggleRecs(app):
    app.enableRec = not app.enableRec
    app.eventMatrix.enableRec = not app.eventMatrix.enableRec
    app.eventMatrix.recR, app.eventMatrix.recC = recommendTime(app)

def eventAvailMode_mousePressed(app, event):
    clickNav(app, event)
    app.inputMatrix.onClick(event)
    app.recButton.onClick(app, event)

def eventAvailMode_mouseReleased(app, event):
    inputReleased = app.inputMatrix.onRelease(event)
    if inputReleased:
        # update the user's availability matrix
        updateUserAvailMatrix(app, app.currentEventID, app.inputMatrix, app.userPriority)
        eventAvailMode_updateEventMatrix(app)

def eventAvailMode_mouseMoved(app, event):
    hoverNav(app, event)
    app.inputMatrix.onHover(event)
    app.recButton.onHover(event)

    eventHover, eventHoverR, eventHoverC = app.eventMatrix.onHover(event)
    if eventHover:
        app.inputAppear = False
        app.usersAppear = True
        usersAvailable(app, eventHoverR, eventHoverC)
    else:
        app.inputAppear = True
        app.usersAppear = False

def eventAvailMode_mouseDragged(app, event):
    app.inputMatrix.onDrag(event)

def eventAvailMode_redrawAll(app, canvas):
    font = "Open Sans", f"{int(app.width/60)}", "italic"
    smallFont = "Open Sans", f"{int(app.width/80)}", "italic"
    drawNav(app, canvas)
    canvas.create_text(app.width*37/48, app.height*19/128, text="group's availability", font=font, fill=app.textC)
    
    if app.inputAppear:
        canvas.create_text(app.width*15/48, app.height*19/128, text="click and drag to input your availability", font=font, fill=app.textC)
        app.inputMatrix.drawMatrix(app, canvas)
    elif app.usersAppear:
        canvas.create_text(app.width*15/48, app.height*19/128, text="USERS AVAILABLE", font=font, fill=app.textC)
        for guest in range(len(app.usersAvailable)):
            canvas.create_text(app.width*15/48, app.height*25/128+30*guest, text=app.usersAvailable[guest], font=smallFont, fill=app.textC)

    app.eventMatrix.drawMatrix(app, canvas)
    app.recButton.drawButton(app, canvas)

def eventAvailMode_sizeChanged(app):
    sizeChanged(app)

##########################################
# Modify Event Page (Host)
##########################################

def modMode_appAttributes(app):
    app.mEarliestAMPM = "AM"
    app.mLatestAMPM = "AM"
    app.modEventTimer = 0
    app.mEarlyTime = False
    app.mLateTime = False
    app.mDaysValid = False
    app.mInviteValid = False

    app.mName = TextBox(app.width/2-100, app.navH+150, app.width/2+100, app.navH+180)
    app.mName.setBgText("set event name")
    app.mDays = TextBox(app.width/2-100, app.navH+220, app.width/2+100, app.navH+250)
    app.mDays.setBgText("enter weekdays")
    app.mEarliest = TextBox(app.width/2-300, app.navH+290, app.width/2-120, app.navH+320)
    app.mEarliest.setBgText("earliest possible time")
    app.mEarlyAM = Bbutton(app.width/2-100, app.navH+290, app.width/2-70, app.navH+320, "AM", setEarlyAM, 
                    bgC="#28DBBB", activeC="#143936", textC="#143936", activeTextC="#28DBBB")
    app.mEarlyPM = Bbutton(app.width/2-50, app.navH+290, app.width/2-20, app.navH+320, "PM", setEarlyPM, 
                    activeC="#28DBBB", activeTextC="#143936")
    app.mLatest = TextBox(app.width/2+20, app.navH+290, app.width/2+200, app.navH+320)
    app.mLateAM = Bbutton(app.width/2+220, app.navH+290, app.width/2+250, app.navH+320, "AM", setLateAM, 
                    bgC="#28DBBB", activeC="#143936", textC="#143936", activeTextC="#28DBBB")
    app.mLatePM = Bbutton(app.width/2+270, app.navH+290, app.width/2+300, app.navH+320, "PM", setLatePM, 
                    activeC="#28DBBB", activeTextC="#143936")
    app.mLatest.setBgText("latest possible time")
    app.mInvite = TextBox(app.width/2-200, app.navH+360, app.width/2+200, app.navH+390)
    app.mInvite.setBgText("search for users to invite (directory below)")

    app.mCreate = Proceed(app.width/2+250, app.navH+360, app.width/2+300, app.navH+390, "-->", dashMode)
    app.mCreated = False

def mSetEarlyAM(app):
    # set PM to off color, set eEarliestAMPM to AM
    app.mEarliestAMPM = "AM"

    app.mEarlyAM.bgC = "#28DBBB"
    app.mEarlyAM.activeC = "#143936"
    app.mEarlyAM.textC = "#143936"
    app.mEarlyAM.activeTextC = "#28DBBB"

    app.mEarlyPM.bgC = ""
    app.mEarlyPM.activeC = "#28DBBB"
    app.mEarlyPM.textC = "#143936"
    app.mEarlyPM.activeTextC = "#143936"

def mSetEarlyPM(app):
    # set AM to off color, set eEarliestAMPM to PM
    app.mEarliestAMPM = "PM"

    app.mEarlyAM.bgC = ""
    app.mEarlyAM.activeC = "#28DBBB"
    app.mEarlyAM.textC = "#143936"
    app.mEarlyAM.activeTextC = "#143936"

    app.mEarlyPM.bgC = "#28DBBB"
    app.mEarlyPM.activeC = "#143936"
    app.mEarlyPM.textC = "#143936"
    app.mEarlyPM.activeTextC = "#28DBBB"

def mSetLateAM(app):
    # set PM to off color, set eEarliestAMPM to AM
    app.mLatestAMPM = "AM"

    app.mLateAM.bgC = "#28DBBB"
    app.mLateAM.activeC = "#143936"
    app.mLateAM.textC = "#143936"
    app.mLateAM.activeTextC = "#28DBBB"

    app.mLatePM.bgC = ""
    app.mLatePM.activeC = "#28DBBB"
    app.mLatePM.textC = "#143936"
    app.mLatePM.activeTextC = "#143936"

def mSetLatePM(app):
    # set AM to off color, set eEarliestAMPM to PM
    app.mLatestAMPM = "PM"

    app.mLateAM.bgC = ""
    app.mLateAM.activeC = "#28DBBB"
    app.mLateAM.textC = "#143936"
    app.mLateAM.activeTextC = "#143936"

    app.mLatePM.bgC = "#28DBBB"
    app.mLatePM.activeC = "#143936"
    app.mLatePM.textC = "#143936"
    app.mLatePM.activeTextC = "#28DBBB"

def modMode_timerFired(app):
    mName = app.mName.inText
    mDays = app.mDays.inText
    mEarliest = app.mEarliest.inText
    mLatest = app.mLatest.inText
    mInvite = app.mInvite.inText
    app.modEventTimer += 1

    if app.modEventTimer%20 == 0:
        app.mName.cursorBlink()
        app.mDays.cursorBlink()
        app.mEarliest.cursorBlink()
        app.mLatest.cursorBlink()
        app.mInvite.cursorBlink()

    app.mDaysValid = weekdaysValid(mDays)
        
    if mEarliest.isdigit() and int(mEarliest)>=0 and int(mEarliest)<=12:
        app.mEarlyTime = True
    else:
        app.mEarlyTime = False
    if mLatest.isdigit() and int(mLatest)>=0 and int(mLatest)<=12:
        app.mLateTime = True
    else:
        app.mLateTime = False

    app.mInviteValid = userSearch(app, mInvite)

    if (mName!="" and mDays!="" and mEarliest!="" and mLatest!="" and mInvite!="" 
        and app.mEarlyTime and app.mLateTime and app.mDaysValid and app.mInviteValid):
        app.mCreate.disabled = False
    else:
        app.mCreate.disabled = True

def modMode_mouseMoved(app, event):
    hoverNav(app, event)
    app.mName.onHover(event)
    app.mDays.onHover(event)
    app.mEarliest.onHover(event)
    app.mLatest.onHover(event)
    app.mInvite.onHover(event)

    app.mEarlyAM.onHover(event)
    app.mEarlyPM.onHover(event)
    app.mLateAM.onHover(event)
    app.mLatePM.onHover(event)

def modMode_mousePressed(app, event):
    mName = app.mName.inText
    mDays = app.mDays.inText
    mEarliest = app.mEarliest.inText
    mLatest = app.mLatest.inText
    mInvite = app.mInvite.inText

    clickNav(app, event)
    app.mName.onClick(app, event)
    app.mDays.onClick(app, event)
    app.mEarliest.onClick(app, event)
    app.mLatest.onClick(app, event)
    app.mInvite.onClick(app, event)

    app.mEarlyAM.onClick(app, event)
    app.mEarlyPM.onClick(app, event)
    app.mLateAM.onClick(app, event)
    app.mLatePM.onClick(app, event)

    if app.mCreate.onClick(app, event):
        # make the weekdays into a processable list
        days = mDays
        dayList = []
        for day in days.split(","):
            day = day.strip().lower()
            dayList += [day]
        # make the times processable
        timeList = []
        early = int(mEarliest)
        late = int(mLatest)
        if app.mEarliestAMPM=="PM":
            early += 12
        if app.mLatestAMPM=="PM":
            late += 12
        for i in range(early, late+1):
            timeList += [i]
        # make the users into a processable list
        users = mInvite
        userList = [app.user]
        for user in users.split(","):
            user = user.strip().lower()
            userList += [user]
        # save event
        id = addEvent(app, mName, dayList, timeList)
        
        for user in userList:
            if user == app.user:
                app.currentUser.invitedEvents += [id]
            userdata = ast.literal_eval(readFile(user+"_invited_events.g"))
            userdata += [id]
            # temporarily generate random priorities for heuristic algorithm
            randPriority = random.randint(0, 7)
            updateUserAvailMatrixGivenName(app, user, id, Matrix(app.width*2/24, app.navH+app.height*2/24, 
                 app.width*13/24, app.navH+app.height*22/24), randPriority)
            writeFile(user+"_invited_events.g", str(userdata))
        # update dashboard events
        dashboardMode_updateEvents(app)
        # clear all app.___.inTexts
        createEventMode_appAttributes(app)

def modMode_keyPressed(app, event):
    app.mName.keysIn(event)
    app.mDays.keysIn(event)
    app.mEarliest.keysIn(event)
    app.mLatest.keysIn(event)
    app.mInvite.keysIn(event)

def modMode_redrawAll(app, canvas):
    mName = app.mName.inText
    mDays = app.mDays.inText
    mEarliest = app.mEarliest.inText
    mLatest = app.mLatest.inText
    mInvite = app.mInvite.inText
    uList = ""
    font = ("Open Sans", 16)

    drawNav(app, canvas)
    canvas.create_text(app.width/2, app.height*27/128, text="CREATE AN EVENT", font=app.titleFont, fill=app.textC)
    app.mName.drawTextBox(app, canvas)
    app.mDays.drawTextBox(app, canvas)
    if not app.mDaysValid and mDays!="":
        canvas.create_text(app.width/2, app.navH+260, text="*Invalid days!", 
            font=font, fill=app.nopeC)

    app.mEarliest.drawTextBox(app, canvas)
    app.mEarlyAM.drawButton(app, canvas)
    app.mEarlyPM.drawButton(app, canvas)
    if not app.mEarlyTime and mEarliest!="":
        canvas.create_text(app.width/2-210, app.navH+330, text="*Invalid time!", 
            font=font, fill=app.nopeC)

    app.mLatest.drawTextBox(app, canvas)
    app.mLateAM.drawButton(app, canvas)
    app.mLatePM.drawButton(app, canvas)
    if not app.mLateTime and mLatest!="":
        canvas.create_text(app.width/2+110, app.navH+330, text="*Invalid time!", 
            font=font, fill=app.nopeC)
    
    app.mInvite.drawTextBox(app, canvas)
    if not app.mInviteValid and mInvite!="":
        canvas.create_text(app.width/2, app.navH+400, text="*Last user not found!", 
            font=font, fill=app.nopeC)
    app.mCreate.drawButton(app, canvas)

    for user in app.accounts:
        uList = uList + "\n" + user
    canvas.create_text(app.width/2, app.navH+430, text=uList, font=font, fill="#137361")

def modMode_sizeChanged(app):
    sizeChanged(app)

##########################################
# Main App
##########################################

def appStarted(app):
    # read data from file
    app.accounts = ast.literal_eval(readFile('accounts.txt'))
    # https://www.programiz.com/python-programming/methods/built-in/eval 
    app.events = eval(readFile('global_events.g'))

    app.titleFont = "Open Sans", f"{int(app.width/30)}"
    app.font = "Open Sans", f"{int(app.width/60)}"
    app.mode = 'landingMode'
    app.timerDelay = 5
    app.makeAnMVCViolation = False
    app.signedIn = False
    app.user = ""
    app.currentUser = None
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
    dashboardMode_appAttributes(app)
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
def eventAvailMode(app, eid):
    if app.signedIn:
        app.currentEventID = eid
        eventAvailMode_updateUserMatrix(app)
        eventAvailMode_updateEventMatrix(app)
        app.mode = "eventAvailMode"
    else:
        app.mode = "signInMode"

# the user is signed in
def setSignedIn(app):
    app.signedIn = True
    # dashboardMode_appAttributes(app)
    # app.mode = "dashboardMode"

# the user is signed out
def setSignedOut(app):
    app.signedIn = False

# sets the current event id
def setCurrentEventID(app, eid):
    app.currentEventID = eid

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

def appStopped(app):
    # save data to file
    if(app.currentUser != None):
        _uname = app.currentUser.username
        _invE = str(app.currentUser.invitedEvents)
        _hostE = str(app.currentUser.myEvents)
        writeFile(_uname + "_invited_events.g", _invE)
        writeFile(_uname + "_hosted_events.g",  _hostE)
        writeFile("global_events.g", str(app.events))
    else:
        print("No user was logged in, so no data was modified. Have a wonderful day. :)\n")

def addEvent(app, name, possibleDays, possibleTimes):
    e = CalendarEvent(name, possibleDays=possibleDays, possibleTimes=possibleTimes)
    app.events[e.id] = e
    app.currentUser.myEvents += [e.id]
    return e.id

def modifyPossibleDatesTimes(app, id, possibleDays, possibleTimes):
    app.events[id].possibleDays = possibleDays
    app.events[id].possibleTimes = possibleTimes

# Adds a user's avaibility to an event
# app -> app context. user-> the user object
# eventId -> id of the event to manipulate
# matrix -> mtx to add, priority -> user priority
def updateUserAvailMatrix(app, eventId, matrix, priority):
    _event = app.events[eventId]
    _event.usersAvail[app.currentUser.username] = (matrix, priority) # (availabilty, priority)

def updateUserAvailMatrixGivenName(app, username, eventId, matrix, priority):
    _event = app.events[eventId]
    _event.usersAvail[username] = (matrix, priority); # (availabilty, priority)

runApp(width=1250, height=750)