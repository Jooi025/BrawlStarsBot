from threading import Thread, Lock
from time import time
import cv2 as cv
from constants import Constants
from ultralytics import YOLO

class Detection:
    # threading properties
    stopped = True
    lock = None

    # properties
    screenshot = None
    results = None
    fps = 0
    avg_fps = 0

    def __init__(self, windowSize, model_file_path, classes, heightScaleFactor):
        """
        Constructor for the Detection class
        """
        # create a thread lock object
        self.lock = Lock()
        # load the trained model
        self.model = YOLO(model_file_path,task="detect")
        self.classes = classes
        self.w = windowSize[0]
        self.h = windowSize[1]
        self.height = heightScaleFactor * self.h

    def find_midpoint(self,x1,y1,x2,y2):
        #x2 > x1
        #y2 > y1
        return [(x1+int((x2-x1)/2),y1+int((y2-y1)/2))]

    def annotate(self,border_size,tile_w,tile_h):
        displacement = 22
        thickness = 2
        # bgr
        red = (0, 0, 255)
        green = (0, 255, 0)
        x_scale = int(self.w/3)
        y_scale = int(self.h/3)
        xBorder = (self.w/tile_w)
        yBorder = (self.h/tile_h)
        size = 2*border_size
        xTop = int(xBorder*((tile_w-size)/2))
        yTop = int(yBorder*((tile_h-size)/2))+displacement
        xBottom = int(xBorder*((tile_w+size)/2))
        yBottom = int(yBorder*((tile_h+size)/2))+displacement
        
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
        self.loop_time = time()
        self.count = 0
        t = Thread(target=self.run)
        t.setDaemon(True)
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
                results = self.model.predict(self.screenshot, imgsz=Constants.imgsz,
                                             half=Constants.half, verbose=False)
                result = results[0]
                for box in result.boxes:
                    x1, y1, x2, y2 = [round(x) for x in box.xyxy[0].tolist()]
                    class_id = int(box.cls[0].item())
                    prob = round(box.conf[0].item(), 2)
                    threshold = Constants.threshold[class_id]
                    if prob >= threshold:
                        midpoint = self.find_midpoint(x1,y1,x2,y2)
                        if self.classes[class_id] == "Player":
                            midpoint =  [( midpoint[0][0], int(midpoint[0][1] + self.height))]
                        if self.classes[class_id] == "Enemy":
                            #standardised enemy height and their label
                            height = y2 - y1
                            y1 = y1 + (height+0.2*self.h)
                            midpoint = [( midpoint[0][0], int(midpoint[0][1] + 0.05*self.h))]
                        tempList[class_id] = tempList[class_id] + midpoint  
                        # draw crosshair
                        cv.drawMarker(self.screenshot, midpoint[0],
                                    red ,thickness=thickness,
                                    markerType= cv.MARKER_CROSS,
                                    line_type=cv.LINE_AA, markerSize=50) 
                        # diplay text
                        cv.putText(self.screenshot, self.classes[class_id], 
                                    midpoint[0], cv.FONT_HERSHEY_SIMPLEX, 0.7, red, 2)    
                # lock the thread while updating the results
                self.lock.acquire()
                self.results = tempList
                self.lock.release()
                self.fps = (1 / (time() - self.loop_time))
                self.loop_time = time()
                self.count += 1
                if self.count == 1:
                    self.avg_fps = self.fps
                else:
                    self.avg_fps = (self.avg_fps*self.count+self.fps)/(self.count + 1)