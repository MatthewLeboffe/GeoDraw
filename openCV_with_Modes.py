from cmu_112_graphics_openCV import *

def appStarted(app):
    app.cameraOpen = False
    app.mode = 'game1'

def game1_keyPressed(app, event):
    if event.key == 'c':
        app.cameraOpen = True
    if event.key == 'm':
        app.mode = 'game2'

def game2_keyPressed(app, event):
    if event.key == 'v':
        app.cameraOpen = False
    if event.key == 'm':
        app.mode = 'game1'

def game1_redrawAll(app, canvas):
    if app.cameraOpen:
        app.drawCamera(canvas)

def game2_redrawAll(app, canvas):
    if app.cameraOpen:
        app.drawCamera(canvas)

runApp(width = 800, height = 400)