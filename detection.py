from threading import Thread, Lock
import torch
from time import sleep
import cv2 as cv
from constants import Constants

class Detection:
    # threading properties
    stopped = True
    lock = None

    # properties
    screenshot = None
    results = None

    def __init__(self, windowSize, model_file_path, classes, heightScaleFactor):
        """
        Constructor for the Detection class
        """
        # create a thread lock object
        self.lock = Lock()
        # load the trained model
        self.model = torch.hub.load("ultralytics/yolov5", 'custom', model_file_path)
        
        if Constants.gpu:
            # use gpu for detection
            self.model.cuda()
        else:
            #us cpu for detection 
            self.model.cpu()

        self.classes = classes
        self.w = windowSize[0]
        self.h = windowSize[1]
        self.height = heightScaleFactor * self.h
    
    def find_midpoint(self,x1,y1,x2,y2):
        #x2 > x1
        #y2 > y1
        return [(x1+int((x2-x1)/2),y1+int((y2-y1)/2))]

    def annotate(self):
        border = 22
        xsplit = 27
        ysplit = 19
        xBorder = self.w/xsplit
        yBorder = self.h/ysplit
        x_scale = int(self.w/3)
        y_scale = int(self.h/3)
        thickness = 2
        red = (0, 0, 255) # bgr
        green = (0, 255, 0)
        size = 3
        xTop = int(xBorder*((xsplit-size)/2))
        yTop = int(yBorder*((ysplit-size)/2))+border
        xBottom = int(xBorder*((xsplit+size)/2))
        yBottom = int(yBorder*((ysplit+size)/2))+border
        
        cv.rectangle(self.screenshot, (xTop, yTop), (xBottom, yBottom), (0,255,0), 2)
        cv.drawMarker(self.screenshot, (int(self.w/2),int((self.h/2)+22)),
                    green ,thickness=thickness,markerType= cv.MARKER_CROSS,
                    line_type=cv.LINE_AA, markerSize=50) 
        #quadrant line
        cv.line(self.screenshot,(x_scale,0),(x_scale,3*y_scale),green,thickness)
        cv.line(self.screenshot,(2*x_scale,0),(2*x_scale,3*y_scale),green,thickness)
        cv.line(self.screenshot,(0,y_scale),(3*x_scale,y_scale),green,thickness)
        cv.line(self.screenshot,(0,2*y_scale),(3*x_scale,2*y_scale),green,thickness)

        if self.results:
            for i in range(len(self.results)):
                    #if the list is not empty
                    if self.results[i]:
                        for cord in self.results[i]:
                            cv.drawMarker(self.screenshot, cord,
                                           red ,thickness=thickness,
                                           markerType= cv.MARKER_CROSS,
                                           line_type=cv.LINE_AA, markerSize=50) 
                            cv.putText(self.screenshot, self.classes[i], 
                                       cord, cv.FONT_HERSHEY_SIMPLEX, 0.7, red, 2)
        #draw midpoint crosshair                    
        cv.drawMarker(self.screenshot, (int(self.w/2),int((self.h/2)+22)),
                        green ,thickness=thickness,markerType= cv.MARKER_CROSS,
                        line_type=cv.LINE_AA, markerSize=50) 
        
    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            if not self.screenshot is None:
                red = (0,0,255)
                thickness = 3
                # create empty nested list
                tempList = len(self.classes)*[[]]
                results = self.model(self.screenshot)
                labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
                self.n = len(labels)
                for i in range(self.n):
                    # player class
                    if labels[i] == 0:
                        threshold = Constants.player_threshold
                    # bush class
                    elif labels[i] == 1:
                        threshold = Constants.bush_threshold
                    # enemy class
                    elif labels[i] == 2:
                        threshold = Constants.enemy_threshold
                    # cube box class
                    elif labels[i] == 3:
                        threshold = Constants.cubebox_threshold
                    row = cord[i]
                    if row[4] >= threshold:
                        x1, y1, x2, y2 = int(row[0] * self.w), int(row[1] * self.h), int(row[2] * self.w), int(row[3] * self.h)
                        midpoint = self.find_midpoint(x1,y1,x2,y2)
                        if self.classes[int(labels[i])] == "Player":
                            midpoint =  [( midpoint[0][0], int(midpoint[0][1] + self.height))]
                        if self.classes[int(labels[i])] == "Enemy":
                            #standardised enemy height and their label
                            height = y2 - y1
                            y1 = y1 + (height+0.2*self.h)
                            midpoint = [( midpoint[0][0], int(midpoint[0][1] + 0.05*self.h))]
                        tempList[int(labels[i])] = tempList[int(labels[i])] + midpoint  
                        # draw crosshair
                        cv.drawMarker(self.screenshot, midpoint[0],
                                    red ,thickness=thickness,
                                    markerType= cv.MARKER_CROSS,
                                    line_type=cv.LINE_AA, markerSize=50) 
                        # diplay text
                        cv.putText(self.screenshot, self.classes[int(labels[i])], 
                                    midpoint[0], cv.FONT_HERSHEY_SIMPLEX, 0.7, red, 2)    
                # lock the thread while updating the results
                self.lock.acquire()
                self.results = tempList
                self.lock.release()
