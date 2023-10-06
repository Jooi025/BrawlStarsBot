import cv2 as cv
from time import time,sleep
from windowcapture import WindowCapture
from detection import Detection
from bot import Brawlbot, BotState
from screendetect import Screendetect, Detectstate
import pyautogui


DEBUG= 1
# brawler characteristic
# change the value for different brawlers
""" 
heightScaleFactor is the pixel distance from midpoint of nametag 
to the midpoint of "circle" divide by the height of window size
"""
heightScaleFactor = 0.154 
speed = 2.4 # units: (tiles per second)
range = 1 # 0 for short, 1 for medium and 2 for long range

# initialize the WindowCapture class
wincap = WindowCapture('Bluestacks App Player')
# get window dimension
windowSize = (wincap.w, wincap.h)

#initialize screendectect classes 
screendetect = Screendetect(windowSize)

#initialize dectection classes 
model_file_path = "BrawlStarsBot/project/best.engine"
classes = ["Player","Bush","Enemy"]
threshold = 0.43
detector=Detection(windowSize, model_file_path, classes,threshold, heightScaleFactor)

#initialize bot class
bot = Brawlbot(windowSize, speed, range)

#start thread
wincap.start()
detector.start()
screendetect.start()
# bot.start()
 
loop_time = time()
while 1:

    if wincap.screenshot is None:
        continue

    detector.update(wincap.screenshot)

    if bot.state == BotState.INITIALIZING:
        bot.update_results(detector.results)
    elif bot.state == BotState.SEARCHING:
        bot.update_results(detector.results)
    elif bot.state == BotState.MOVING:
        bot.update_screenshot(wincap.screenshot)
        bot.update_results(detector.results)
    elif bot.state == BotState.HIDING:
        bot.update_results(detector.results)


    if screendetect.state ==  Detectstate.EXIT or screendetect.state ==  Detectstate.PLAY:
        print("stop bot")
        pyautogui.mouseUp(button = "right")
        bot.stop()
    if screendetect.state ==  Detectstate.LOAD:
        print("start bot")
        bot.timestamp = time()
        bot.state = BotState.INITIALIZING
        bot.start()
        #wait for game to load
        sleep(3)

    #for DEBUG purposes
    if DEBUG:
        fps=(1 / (time() - loop_time))
        annotated_image = detector.annotate(fps)
        cv.imshow("Brawl Stars Bot",annotated_image)
        loop_time = time()

    # Press q to exit the script                                      
    key = cv.waitKey(1)
    if key == ord('q'):
        #stop all threads
        wincap.stop()
        detector.stop()
        screendetect.stop()
        bot.stop()
        cv.destroyAllWindows()
        break
print('Done.')