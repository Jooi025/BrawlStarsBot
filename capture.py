import cv2 as cv
from time import time
from modules.windowcapture import WindowCapture
from constants import Constants

# initialize the WindowCapture class
wincap = WindowCapture(Constants.window_name)
wincap.set_window()

while(True):
    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    cv.imshow("YOLOv8", screenshot)
    loop_time = time()

    # press 'q' with the output window focused to exit.
    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows()
        break
print('Done.')
