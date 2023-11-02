import cv2 as cv
from time import time,sleep
from windowcapture import WindowCapture
from detection import Detection
from bot import Brawlbot, BotState
from screendetect import Screendetect, Detectstate
import pyautogui
import os
from constants import Constants

def main():
    DEBUG = 1
    
    # initialize the WindowCapture class
    wincap = WindowCapture(Constants.window_name)
    # get window dimension
    windowSize = (wincap.w, wincap.h)
    
    #initialize screendectect classes 
    screendetect = Screendetect(windowSize)

    #initialize dectection classes 
    classes = ["Player","Bush","Enemy"]
    threshold = 0.34
    detector=Detection(windowSize, Constants.model_file_path, classes, threshold, Constants.heightScaleFactor)

    #initialize bot class
    bot = Brawlbot(windowSize, Constants.speed, Constants.range)
    # set target window as foreground
    wincap.set_window()

    #start thread
    wincap.start()
    detector.start()
    # screendetect.start()
    # bot.start()
    
    loop_time = time()
    while True:
        if wincap.screenshot is None:
            continue
        
        # update screenshot to detector 
        detector.update(wincap.screenshot)

        # check bot stae
        if bot.state == BotState.INITIALIZING:
            bot.update_results(detector.results)
        elif bot.state == BotState.SEARCHING:
            bot.update_results(detector.results)
        elif bot.state == BotState.MOVING:
            bot.update_screenshot(wincap.screenshot)
            bot.update_results(detector.results)
        elif bot.state == BotState.HIDING:
            bot.update_results(detector.results)

        # check screendetect state
        if screendetect.state ==  Detectstate.EXIT or screendetect.state ==  Detectstate.PLAY:
            print("stop bot")
            pyautogui.mouseUp(button = "right")
            bot.stop()
        if screendetect.state ==  Detectstate.LOAD:
            print("start bot")
            bot.timestamp = time()
            bot.state = BotState.INITIALIZING
            #wait for game to load
            sleep(7)
            bot.start()

        # display annotated window with FPS
        if DEBUG:
            try:
                fps=(1 / (time() - loop_time))
            except ZeroDivisionError:
                fps = 0.01
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

while True:
    print("1. Start Bot")
    print("2. Set shutdown timer")
    print("3. Cancel shutdown timer")
    print("4. Exit")
    user_input = input("Select: ")
    print("")

    # run the bot
    if user_input == "1":
        main()

    # use cmd to start a shutdown timer 
    elif user_input == "2":
        try:
            hour = int(input("How many hour before shutdown? "))
            second = 3600 * hour
            os.system(f'cmd /c "shutdown -s -t {second}"')
            print(f"Shuting down in {hour} hour")
        except ValueError:
            print("Please enter a valid input!")

    # use cmd to cancel shutdown timer
    elif user_input == "3":
        os.system('cmd /c "shutdown -a"')
        print("Shutdown timer cancelled")

    # exit
    elif user_input =="4":
        print("Exitting")
        break

    print("")