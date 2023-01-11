####################################################

#                 WELCOME TO GEODRAW

####################################################



# this is the main file to run in order to grade/play the game

import matplotlib.pyplot as plt
from cmu_112_graphics_openCV import *
import math
import numpy as np

import shapes
from trackingCode import *
import time

def gameDimensions():
    width = 600
    height = 450
    return width, height

def sortPoints(listCoords):
    #sorts by angle from 0 radii
    return sorted(listCoords, key=lambda i: i[-1])

'''
to score how accurate a user drew we are going to use some basic trig. 
Basically to tell if a point is between 2 lines, the distance between point A and
point C has to = the distance from AB to BC. if this is true than the point is on the line. 
However there needs to be a range of error since == would consider only pixel perfect drawings
so we need to adjust the range of what is considered correct. 
''' 

def score(app):
    correctPoints = 0
    for point in range(len(app.polyCoords) - 1):
        for oldLoc in app.oldLocations:
            polygonC1 = app.polyCoords[point][:2]
            polygonC2 = app.polyCoords[point + 1][:2]
            correctDistance = math.dist(polygonC1, polygonC2)
            ABdist = math.dist(polygonC1, oldLoc)
            BCdist = math.dist(polygonC2, oldLoc)

            if correctDistance * (1 - app.scoreRange) < (ABdist + BCdist) < correctDistance * (1 + app.scoreRange):
                correctPoints += 1
    
    return correctPoints / (len(app.oldLocations) + 1)

def imageDict(app):
    images = dict()
    images["logo"] = app.loadImage('images/startLogo.png')
    images["startBtn"] = app.scaleImage(app.loadImage('images/startBTN.png'), 3/8)
    images["howtoplay"] = app.scaleImage(app.loadImage('images/howtoplay.png'), 3/8)
    images["quit"] = app.scaleImage(app.loadImage('images/quit.png'), 3/8)
    images["scoreDrawing"] = app.scaleImage(app.loadImage('images/scoreDrawing.png'), 3/8)
    images["restart"] = app.scaleImage(app.loadImage('images/restart.png'), 3/8)
    images['difficulty'] = app.loadImage('images/difficulty.png')
    images['tutorial'] = app.loadImage('images/tutorial.png')
    images['end'] = app.loadImage('images/end.png')

    return images

def appStarted(app):
    app.images = imageDict(app)
    app.timerDelay = 1 #miliseconds
    app.width, app.height = gameDimensions()
    app.center = (app.width // 2, app.height // 2)
    
    #screens
    app.startScreen = True
    app.tutorialScreen = False
    app.difficultyScreen = False
    app.roundScreen = False
    app.gameScreen = False
    app.endScreen = False

    #default difficulty values
    app.finalRound = 5
    app.maxTime = 120
    app.scoreRange = 0.1

    app.round = 1
    app.roundStart = time.time() + 3
    app.savedTime = 0

    app.roundScore = 0
    app.totalScore = 0
    app.roundSize = 30


    app.poly = shapes.Polygon(app.round + 2, app.width, app.height)
    app.polyPoints = app.poly.edges

    app.polyCoords = sortPoints(app.poly.points)

    app.trackingLocation = list(drawBox(getImg(), getBbox()))
    app.showPoly = True

    app.oldLocations = []


def drawStartScreen(app, canvas):
    logox = app.width / 2
    logoy = app.height / 2 - app.height * 0.2
    canvas.create_image(logox, logoy, image=ImageTk.PhotoImage(app.images['logo']))
    
    starty = logoy + app.height * 0.4
    canvas.create_image(logox, starty, image=ImageTk.PhotoImage(app.images['startBtn']))

    tutorialy = starty + app.height * 0.1
    canvas.create_image(logox, tutorialy, image=ImageTk.PhotoImage(app.images['howtoplay']))

    quity = tutorialy + app.height * 0.1
    canvas.create_image(logox, quity, image=ImageTk.PhotoImage(app.images['quit']))

def drawPoly(app, canvas):
    if app.showPoly:
        cx = app.center[0]
        cy = app.center[1]
        canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, fill="black")
        listLen = len(app.polyCoords)

        for i in range(0, listLen):

            x0 = app.polyCoords[i][0]
            y0 = app.polyCoords[i][1]

            canvas.create_oval(x0 - 4, y0 - 4, x0 + 4, y0 + 4)

            x1 = app.polyCoords[(i + 1) % listLen][0]
            y1 = app.polyCoords[(i + 1) % listLen][1]

            canvas.create_line(x0, y0, x1, y1, width=4, fill='black')

def drawGame(app, canvas):
    #draws camera view on canvas
    app.drawCamera(canvas)    

    drawPoly(app, canvas)
    canvas.create_text(app.width / 2, 25, text= f'Total score: {app.totalScore}', font='Arial 24 bold', fill="lime")
    canvas.create_text(app.width / 2, 55, text= f'Current score: {app.roundScore}', font='Arial 16 bold', fill="lime")
    
    try:
        x,y,w,h = app.trackingLocation
        canvas.create_rectangle((x, y), (x + w, y + h))
    except:
        pass

    
    for spot in range(len(app.oldLocations) - 1):

        x0 = app.oldLocations[spot][0]
        y0 = app.oldLocations[spot][1]

        x1 = app.oldLocations[spot + 1][0]
        y1 = app.oldLocations[spot + 1][1]
        canvas.create_line(x0, y0, x1, y1, fill="lime", width = 5)

    canvas.create_image(app.width - 50, app.height - 50, image=ImageTk.PhotoImage(app.images['restart']))
    canvas.create_image(app.width - 120, app.height - 50, image=ImageTk.PhotoImage(app.images['scoreDrawing']))

    t = app.maxTime - int(time.time() - app.roundStart)
    canvas.create_text(100, app.height - 15, text=f'Time Remaining: {t}', font='Arial 14 bold', fill="lime")

def drawIntroScreen(app, canvas):
    app.drawCamera(canvas)
    if app.round == app.finalRound:
        canvas.create_text(app.width / 2, app.height / 2, text= f'Final Round!', font=f'Arial {app.roundSize} bold', fill="lime")
    elif app.roundSize < 59:
        canvas.create_text(app.width / 2, app.height / 2, text= f'ROUND {app.round}', font=f'Arial {app.roundSize} bold', fill="lime")
    elif app.round == 1:
        canvas.create_text(app.width / 2, app.height / 2, text= "START!", font=f'Arial 50 bold', fill="lime")
        time.sleep(1)

def drawDifficultyScreen(app, canvas):
    canvas.create_image(app.center, image=ImageTk.PhotoImage(app.images['difficulty']))

def drawTutorialScreen(app, canvas):
    canvas.create_image(app.center, image=ImageTk.PhotoImage(app.images['tutorial']))

def drawEndScreen(app, canvas):
    app.drawCamera(canvas)
    canvas.create_image(app.center, image=ImageTk.PhotoImage(app.images['end']))
    canvas.create_text(app.width / 2, app.height - 25, text= f'Final Score: {app.totalScore}', font=f'Arial 30 bold', fill="lime")

def redrawAll(app, canvas):
    if app.startScreen:
        drawStartScreen(app, canvas)
    elif app.tutorialScreen:
        drawTutorialScreen(app, canvas)
    elif app.roundScreen:
        drawIntroScreen(app, canvas)
    elif app.difficultyScreen:
        drawDifficultyScreen(app, canvas)
    elif app.gameScreen: 
        drawGame(app, canvas)
    elif app.endScreen:
        drawEndScreen(app, canvas)
    
    
def timerFired(app):
    if app.roundScreen:
        if app.roundSize < 60:
            app.roundSize += 1
        else:
            app.roundScreen = not app.roundScreen
            app.gameScreen = not app.gameScreen

    

def cameraFired(app):
    app.roundScore = int(score(app) * app.round * 1000)
    app.trackingLocation = track(app.frame)
    try:
        x,y,w,h = app.trackingLocation
        cx = (x + (x + w)) / 2
        cy = (y + (y + h)) / 2
        app.oldLocations.append((cx, cy))
    except:
        pass

    if (app.maxTime - int(time.time() - app.roundStart)) == 0:
        update(app)


def keyPressed(app, event):
    #debugging keypresses
    if event.key == 'r':
        appStarted(app)
    if event.key == "h":
        app.showPoly = not app.showPoly
    if event.key == "l":
        app.oldLocations = []
    if event.key == "Space":
        app.totalScore += app.roundScore
        app.round += 1
        app.poly = shapes.Polygon(app.round + 2, app.width, app.height)
        app.polyPoints = app.poly.edges
        app.polyCoords = sortPoints(app.poly.points)
        app.roundScreen = not app.roundScreen
        app.gameScreen = not app.gameScreen
        app.roundStart = time.time()

    if event.key == "q":
        cap.release()
        cv2.destroyAllWindows()
        exit()

def update(app):
    app.round += 1
    app.totalScore += int(app.roundScore * 0.05 * (app.maxTime - int(time.time() - app.roundStart)))
    app.poly = shapes.Polygon(app.round + 2, app.width, app.height)
    app.polyPoints = app.poly.edges
    app.polyCoords = sortPoints(app.poly.points)
    app.roundSize = 30
    app.roundStart = time.time()
    app.oldLocations = []
    if app.round > app.finalRound:
        app.endScreen = True
        app.gameScreen = False
    else:
        app.roundScreen = not app.roundScreen
        app.gameScreen = not app.gameScreen

def clickedStartScreen(app, x, y):
    if 206 <= x <= 393:
            if 296 <= y <= 333:
                app.startScreen = False
                app.difficultyScreen = True
                app.oldLocations = []
            elif 341 <= y <= 378:
                app.startScreen = False
                app.tutorialScreen = True
            elif 386 <= y <= 423:
                cap.release()
                cv2.destroyAllWindows()
                exit()

def clickedDifficultyScreen(app, x, y):
    if 110 <= y <= 255:
        if 52 <= x <= 183:
            app.finalRound = 5
            app.maxTime = 120
            app.scoreRange = 0.1
        elif 236 <= x <= 363:
            app.finalRound = 10
            app.maxTime = 60
            app.scoreRange = 0.08
        elif 415 <= x <= 551:
            app.finalRound = 15
            app.maxTime = 10
            app.scoreRange = 0.05
    
    app.difficultyScreen = False
    app.roundScreen = True
    
def clickedGameScreen(app, x, y):
    if 365 <= y <= 430:
            if 451 <= x <= 510:
                update(app)
                
                
            elif 523 <= x <= 581:
                app.oldLocations = []

def clickedTutorialScreen(app, x, y):
    if 541 <= x <= 584 and 17 <= y <= 58:
        app.tutorialScreen = False
        app.startScreen = True

def mousePressed(app, event):
    x, y = event.x, event.y
    if app.startScreen: 
        clickedStartScreen(app, x, y)
    elif app.difficultyScreen: 
        clickedDifficultyScreen(app, x, y)
    elif app.tutorialScreen: 
        clickedTutorialScreen(app, x, y)
    elif app.gameScreen: 
        clickedGameScreen(app, x, y)
                      
def runGame():
    width, height = gameDimensions()
    runApp(width= width, height= height)

def main():
    runGame()

if __name__ == '__main__':
    main()