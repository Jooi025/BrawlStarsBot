import cv2 as cv
from time import time,sleep
from modules.windowcapture import WindowCapture
from modules.bot import Brawlbot, BotState
from modules.screendetect import Screendetect, Detectstate
from modules.detection import Detection
from modules.print import bcolors
import pyautogui as py
import os
from constants import Constants

def stop_all_thread(wincap,screendetect,bot,detector):
    """
    stop all thread from running
    """
    py.mouseUp(button = Constants.movement_key)
    wincap.stop()
    detector.stop()
    screendetect.stop()
    bot.stop()
    cv.destroyAllWindows()

def add_two_tuple(tup1,tup2):
    """
    add two tuples
    """
    if not(tup1 is None or tup2 is None):
        return tuple(map(sum, zip(tup1, tup2)))

def main():
    # initialize the WindowCapture class
    wincap = WindowCapture(Constants.window_name)
    # get window dimension
    windowSize = wincap.get_dimension()
    # set target window as foreground
    sleep(0.5)
    wincap.set_window()

    # initialize detection class
    detector = Detection(windowSize,Constants.model_file_path,Constants.classes,Constants.heightScaleFactor)
    # initialize screendectect class
    screendetect = Screendetect(windowSize,wincap.offsets)
    # initialize bot class
    bot = Brawlbot(windowSize, wincap.offsets, Constants.speed, Constants.attack_range)
    
    # move cursor to the middle of bluestacks
    middle_of_window = (int(wincap.w/2+wincap.offset_x),int(wincap.h/2+wincap.offset_y))
    py.moveTo(middle_of_window[0],middle_of_window[1])

    #start thread
    wincap.start()
    detector.start()
    screendetect.start()
    
    print(f"Resolution: {wincap.screen_resolution}")
    print(f"Window Size: {windowSize}")
    print(f"Scaling: {wincap.scaling*100}%")

    aspect_ratio = windowSize[0]/windowSize[1]
    if aspect_ratio > 1.79:
        print(bcolors.WARNING + "Please make sure to disable ads on bluestack and close the right sidebar for the bot to work as intended." + bcolors.ENDC)

    while True:
        screenshot = wincap.screenshot
        if screenshot is None:
            continue
        # update screenshot for dectector
        detector.update(screenshot)
        screendetect.update_bot_stop(bot.stopped)
        # check bot state
        if bot.state == BotState.INITIALIZING:
            bot.update_results(detector.results)
        elif bot.state == BotState.SEARCHING:
            bot.update_results(detector.results)
        elif bot.state == BotState.MOVING:
            bot.update_screenshot(screenshot)
            bot.update_results(detector.results)
        elif bot.state == BotState.HIDING:
            bot.update_results(detector.results)
            bot.update_player(add_two_tuple(detector.player_topleft,wincap.offsets)
                              ,add_two_tuple(detector.player_bottomright,wincap.offsets))
        elif bot.state == BotState.ATTACKING:
            bot.update_results(detector.results)

        # check screendetect state
        if (screendetect.state ==  Detectstate.EXIT
            or screendetect.state ==  Detectstate.PLAY_AGAIN
            or screendetect.state ==  Detectstate.CONNECTION
            or screendetect.state ==  Detectstate.PLAY
            or screendetect.state == Detectstate.PROCEED):
            py.mouseUp(button = Constants.movement_key)
            bot.stop()
        elif screendetect.state ==  Detectstate.LOAD:
            if bot.stopped:
                #wait for game to load
                sleep(4)
                print("starting bot")
                # reset timestamp and state
                bot.timestamp = time()
                bot.state = BotState.INITIALIZING
                bot.start()

        # display annotated window with FPS
        if Constants.DEBUG:
            detector.annotate_detection_midpoint()
            detector.annotate_border(bot.border_size,bot.tile_w,bot.tile_h)
            detector.annotate_fps(wincap.avg_fps)
            cv.imshow("Brawl Stars Bot",detector.screenshot)

        # Press q to exit the script
        key = cv.waitKey(1)
        x_mouse, y_mouse = py.position()
        if wincap.screen_resolution[1] == (windowSize[1]+wincap.titlebar_pixels+1):
            stop_bool = x_mouse > (wincap.offset_x + wincap.w)
        else:
            stop_bool = ((x_mouse > 0 and x_mouse < wincap.left and y_mouse > 0 and y_mouse < wincap.top)
            or ( x_mouse > wincap.right and x_mouse < wincap.screen_resolution[0]
                and y_mouse > wincap.bottom and y_mouse < wincap.screen_resolution[1]))
        
        if (key == ord('q') or stop_bool):
            #stop all threads
            stop_all_thread(wincap,screendetect,bot,detector)
            break
    print(bcolors.WARNING +'Cursor currently not on Bluestacks, exiting bot...' +bcolors.ENDC)
    stop_all_thread(wincap,screendetect,bot,detector)

if __name__ == "__main__":
    print(" ")
    print(bcolors.HEADER + bcolors.BOLD +
              "Before starting the bot, make sure you have Brawl Stars open \non Bluestacks and selected solo showdown gamemode.")
    print("")
    print("Also make sure to change the speed, attack_range and HeightScaleFactor"
            +"\nfor you selected brawler at constants.py (instruction there as well).")
    print("To exit bot hover cursor to the top left or bottom right corner.")
    print("")
    print(bcolors.UNDERLINE + "IMPORTANT - make sure to disable ads on bluestack and close the right sidebar" + bcolors.ENDC)
    while True:
        print("")
        print("1. Start Bot")
        print("2. Set shutdown timer")
        print("3. Cancel shutdown timer")
        print("4. Exit")
        user_input = input("Select: ").lower()
        print("")
        # run the bot
        if user_input == "1" or user_input == "start bot":
            main()
        # use cmd to start a shutdown timer
        elif user_input == "2" or user_input == "set shutdown timer":
            print("Set Shutdown Timer")
            try:
                hour = int(input("How many hour before shutdown? "))
                second = 3600 * hour
                os.system(f'cmd /c "shutdown -s -t {second}"')
                print(f"Shuting down in {hour} hour")
            except ValueError:
                print("Please enter a valid input!")
        # use cmd to cancel shutdown timer
        elif user_input == "3" or user_input == "cancel shutdown timer":
            os.system('cmd /c "shutdown -a"')
            print("Shutdown timer cancelled")
        # exit
        elif user_input =="4" or user_input == "exit":
            print("Exitting...")
            break