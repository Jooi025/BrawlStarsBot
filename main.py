import cv2 as cv
from time import time,sleep
from windowcapture import WindowCapture
from bot import Brawlbot, BotState
from screendetect import Screendetect, Detectstate
from detection import annotate,detection
import pyautogui
import os
from constants import Constants
import torch

def main():
    DEBUG = 1
    # initialize the WindowCapture class
    wincap = WindowCapture(Constants.window_name)
    # get window dimension
    windowSize = (wincap.w, wincap.h)

    #initialize screendectect classes 
    screendetect = Screendetect(windowSize)

    #initialize bot class
    bot = Brawlbot(windowSize, Constants.speed, Constants.range)
    
    # set target window as foreground
    sleep(0.5)
    wincap.set_window()

    model = torch.hub.load("ultralytics/yolov5", 'custom', Constants.model_file_path)
    if Constants.gpu:
        # use gpu for detection
        model.cuda()
    else:
        #us cpu for detection 
        model.cpu()
    
    #start thread
    wincap.start()
    screendetect.start()
    bot.start()
    
    loop_time = time()
    classes = Constants.classes
    while True:
        screenshot = wincap.screenshot

        if screenshot is None:
            continue

        screenshot,detection_cord = detection(model,classes,screenshot,windowSize)     

        # check bot state
        if bot.state == BotState.INITIALIZING:
            bot.update_results(detection_cord)
        elif bot.state == BotState.SEARCHING:
            bot.update_results(detection_cord)
        elif bot.state == BotState.MOVING:
            bot.update_screenshot(screenshot)
            bot.update_results(detection_cord)
        elif bot.state == BotState.HIDING:
            bot.update_results(detection_cord)
        elif bot.state == BotState.ATTACKING:
            bot.update_results(detection_cord)

        # check screendetect state
        if screendetect.state ==  Detectstate.EXIT or screendetect.state ==  Detectstate.PLAY:
            print("stop")
            pyautogui.mouseUp(button = Constants.movement_key)
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
                fps = 30
            screenshot = annotate(windowSize,screenshot,fps)
            cv.imshow("Brawl Stars Bot",screenshot)
            loop_time = time()

        # Press q to exit the script                                      
        key = cv.waitKey(1)
        x_pos,y_pos = pyautogui.position()
        if key == ord('q') or (x_pos>windowSize[0] or y_pos>windowSize[1]):
            #stop all threads
            wincap.stop()
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