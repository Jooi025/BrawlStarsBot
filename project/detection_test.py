import cv2 as cv
import numpy as np
from time import time,sleep
from windowcapture import WindowCapture
import torch



# model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Users/josep/Desktop/yolov5 brawl/yolov5/static/best.pt', force_reload=True)
# model = torch.hub.load('ultralytics/yolov5', 'custom', 'static3/best.onnx')
model = torch.hub.load('ultralytics/yolov5', 'custom', 'project/best.engine',force_reload=True)
# initialize the WindowCapture class
wincap = WindowCapture('Bluestacks App Player')
#get window dimension
w,h=wincap.get_dimension()

#object detection
classes = ["Player","Bush","Enemy"]

model.cuda()
model.multi_label = False

loop_time = time()

while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()
    
    results = model(screenshot)
    labels, cord = results.xyxyn[0][:, -1].cpu().numpy(), results.xyxyn[0][:, :-1].cpu().numpy()
	
    n = len(labels)
    bgr = (0, 255,0)
    for i in range(n):
        row = cord[i]
        if row[4] >= 0.5:
            x1, y1, x2, y2 = int(row[0] * w), int(row[1] * h), int(row[2] * w), int(row[3] * h)
            cv.rectangle(screenshot, (x1, y1), (x2, y2), bgr, 2)
            cv.putText(screenshot, classes[int(labels[i])], (x1, y1), cv.FONT_HERSHEY_SIMPLEX, 0.7, bgr, 2)

    # debug the loop rate
    fps=(1 / (time() - loop_time))
    cv.putText(screenshot,f"FPS:{int(fps)}",(20,h-20),cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv.imshow("YOLOv5", screenshot)
    loop_time = time()

    # press 'q' with the output window focused to exit.
    screenshotPath=" "
    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows()
        break
    elif key == ord('f'):
        cv.imwrite(screenshotPath+'/{}.jpg'.format(loop_time), screenshot)
print('Done.')