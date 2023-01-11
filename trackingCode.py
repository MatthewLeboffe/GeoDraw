#This is the tracking file. It is responsible for tracking the object using 
# ROI and outputs the coordinates of said object to main.py

import cv2

cap = cv2.VideoCapture(0)

tracker = cv2.legacy_TrackerMOSSE.create()
success, img = cap.read()

# select a bounding box ( ROI )
bbox = cv2.selectROI("Tracking", img, False)
tracker.init(img, bbox)


def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    return x, y, w, h 

def getImg():
    return img

def getBbox():
    return bbox

def track(img):
    timer = cv2.getTickCount()

    success, bbox = tracker.update(img)

    if success:
        return drawBox(img, bbox)
    