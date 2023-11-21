import cv2 as cv
from time import sleep
from windowcapture import WindowCapture
from detection import Detection
from constants import Constants

wincap = WindowCapture(Constants.window_name)
# get window dimension
windowSize = wincap.get_dimension()
# set target window as foreground
sleep(0.5)
wincap.set_window()

# initialize detection class
detector = Detection(windowSize,Constants.model_file_path,Constants.classes,Constants.heightScaleFactor)

wincap.start()
detector.start()

print(f"Resolution: {wincap.screen_resolution}")
print(f"Window Size: {windowSize}")
print(f"Scaling: {wincap.scaling*100}%")

while(True):
    screenshot = wincap.screenshot
    if screenshot is None:
        continue
    detector.update(screenshot)
    detector.annotate_detection_midpoint()
    detector.annotate_fps(wincap.avg_fps)
    cv.imshow("Detection test",detector.screenshot)

    # press 'q' with the output window focused to exit.
    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows()
        break
print('Done.')