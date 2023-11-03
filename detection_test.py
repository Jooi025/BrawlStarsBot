import cv2 as cv
from time import time
from windowcapture import WindowCapture
import torch
from constants import Constants

model = torch.hub.load('ultralytics/yolov5', 'custom', Constants.model_file_path,force_reload=True)
if Constants.gpu:
    # use gpu for detection
    model.cuda()

# initialize the WindowCapture class
wincap = WindowCapture(Constants.window_name)
#get window dimension
w,h=wincap.get_dimension()

#object detection
classes = Constants.classes
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
        if row[4] >= Constants.threshold:
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