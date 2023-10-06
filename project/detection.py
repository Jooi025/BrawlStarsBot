from threading import Thread, Lock
import torch
from time import sleep
import cv2 as cv


class Detection:
    # threading properties
    stopped = True
    lock = None

    # properties
    screenshot = None
    results = None

    def __init__(self, windowSize, model_file_path, classes , threshold , heightScaleFactor):
        """
        Constructor for the Detection class
        """
        # create a thread lock object
        self.lock = Lock()
        # load the trained model
        self.model = torch.hub.load("ultralytics/yolov5", 'custom', model_file_path)
        # use gpu for dectection
        self.model.cuda()

        self.classes = classes
        self.w = windowSize[0]
        self.h = windowSize[1]
        self.threshold = threshold
        self.height = heightScaleFactor * self.h
    
    def find_midpoint(self,x1,y1,x2,y2):
        #x2 > x1
        #y2 > y1
        return [(x1+int((x2-x1)/2),y1+int((y2-y1)/2))]

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
                # create empty nested list
                tempList= len(self.classes)*[[]]
                results = self.model(self.screenshot)
                self.labels, self.cord = results.xyxyn[0][:, -1].cpu().numpy(), results.xyxyn[0][:, :-1].cpu().numpy()
                self.n = len(self.labels)
                for i in range(self.n):
                    row = self.cord[i]
                    if row[4] >= self.threshold:
                        x1, y1, x2, y2 = int(row[0] * self.w), int(row[1] * self.h), int(row[2] * self.w), int(row[3] * self.h)
                        midpoint = self.find_midpoint(x1,y1,x2,y2)
                        if self.classes[int(self.labels[i])] == "Player":
                            midpoint =  [( midpoint[0][0], int(midpoint[0][1] + self.height))]
                        if self.classes[int(self.labels[i])] == "Enemy":
                            #standardised enemy height and their label
                            height = y2 - y1
                            y1 = y1 + (height+0.2*self.h)
                            midpoint = [( midpoint[0][0], int(midpoint[0][1] + 0.05*self.h))]
                        tempList[int(self.labels[i])] = tempList[int(self.labels[i])] + midpoint      
                # lock the thread while updating the results
                self.lock.acquire()
                self.results = tempList
                sleep(0.01)
                self.lock.release()
    
    def annotate(self,fps):
        sleep(0.001)
        red = (0, 0, 255) # bgr
        green = (0, 255, 0)
        if self.results:
            for i in range(len(self.results)):
                    #if the list is not empty
                    if self.results[i]:
                        for cord in self.results[i]:
                            cv.drawMarker(self.screenshot, cord , red ,thickness=1,markerType= cv.MARKER_CROSS,
                                        line_type=cv.LINE_AA, markerSize=50) 
                            cv.putText(self.screenshot, self.classes[i], cord, cv.FONT_HERSHEY_SIMPLEX, 0.7, red, 2)
        #draw midpoint crosshair                    
        cv.drawMarker(self.screenshot, (int(self.w/2),int((self.h/2)+22)), green ,thickness=1,markerType= cv.MARKER_CROSS,
                                    line_type=cv.LINE_AA, markerSize=50) 
        #display FPS
        cv.putText(self.screenshot,f"FPS:{int(fps)}",(20,self.h-20),cv.FONT_HERSHEY_SIMPLEX, 1, green, 2)
        return self.screenshot
