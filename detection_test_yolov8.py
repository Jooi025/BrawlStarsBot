import cv2 as cv
from time import time
from windowcapture import WindowCapture
from constants import Constants
from ultralytics import YOLO

model = YOLO("yolov8_model\\yolov8.engine",task="detect")
# initialize the WindowCapture class
wincap = WindowCapture(Constants.window_name)
#get window dimension
w, h=wincap.get_dimension()

#object detection
classes = Constants.classes
loop_time = time()
bgr = (0,255,0)

while(True):
    # get an updated image of the game
    screenshot = wincap.get_screenshot()
    results = model.predict(screenshot, verbose=False)
    result = results[0]
    for box in result.boxes:
        x1, y1, x2, y2 = [round(x) for x in box.xyxy[0].tolist()]
        class_id = box.cls[0].item()
        prob = round(box.conf[0].item(), 2)
        if class_id == 0:
            threshold = Constants.player_threshold
        # bush class
        elif class_id == 1:
            threshold = Constants.bush_threshold
        # enemy class
        elif class_id == 2:
            threshold = Constants.enemy_threshold
        # cube box class
        elif class_id == 3:
            threshold = Constants.cubebox_threshold
        if prob >= threshold:
            cv.rectangle(screenshot, (x1, y1), (x2, y2), bgr, 2)
            cv.putText(screenshot, f"{result.names[class_id]}: {prob}", (x1, y1), cv.FONT_HERSHEY_SIMPLEX, 0.7, bgr, 2)

    # # debug the loop rate
    fps=(1 / (time() - loop_time))
    cv.putText(screenshot,f"FPS:{int(fps)}",(20,h-20),cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv.imshow("YOLOv8", screenshot)
    loop_time = time()

    # press 'q' with the output window focused to exit.
    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows()
        break
print('Done.')