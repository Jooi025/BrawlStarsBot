import pydirectinput as py
import pyautogui
from threading import Thread, Lock
from time import sleep
from constants import Constants

"""
IDLE: When state exit,play and load is finished, state is changed to IDLE so 
it doesn't spam the terminal with print.

DETECT: Actively check if player is defeated, play again button and loading in.

EXIT: When brawler is defeated, exit the match and stop the bot.

PLAY: When play again is showed, press it and stop the bot.

LOAD: When loading into the match, start the bot
"""
class Detectstate:
    IDLE = 0
    DETECT = 1
    EXIT = 2
    PLAY = 3
    LOAD = 4
    
class Screendetect:
    #RGB value
    defeatedColor = (62,0,0)
    playColor = (224, 186, 8)
    loadColor = (177, 239, 74)
    defeated_xScale = 0.9677
    defeated_yScale = 0.2285
    def __init__(self,windowSize,offset) -> None:
        """
        Constructor for the Screendectect class
        """
        self.state = Detectstate.DETECT
        self.lock = Lock()
        self.w = windowSize[0]
        self.h = windowSize[1]
        self.offset_x = offset[0]
        self.offset_y = offset[1]
        self.defeated = (round(self.w*0.9683)+self.offset_x, round(self.h*0.1969)+self.offset_y)
        self.playButton = (round(self.w*0.5903)+self.offset_x, round(self.h*0.9197)+self.offset_y)
        self.exitButton = (round(self.w*0.493)+self.offset_x, round(self.h*0.9187)+self.offset_y)
        self.loadButton = (round(self.w*0.084)+self.offset_x, round(self.h*0.1319)+self.offset_y)
    
    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.setDaemon(True)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            if self.state == Detectstate.IDLE:
                sleep(3)
                self.state = Detectstate.DETECT
            
            elif self.state == Detectstate.DETECT:
                sleep(0.01)
                # using try because there
                try:
                    if pyautogui.pixelMatchesColor(self.playButton[0], self.playButton[1],self.playColor,tolerance=15):
                        print("Playing again")
                        self.lock.acquire()
                        self.state = Detectstate.PLAY
                        self.lock.release()
                    elif pyautogui.pixelMatchesColor(self.loadButton[0], self.loadButton[1],self.loadColor,tolerance=20):
                        print("Loading in")
                        self.lock.acquire()
                        sleep(3)
                        self.state = Detectstate.LOAD
                        self.lock.release()
                    elif pyautogui.pixelMatchesColor(self.defeated[0], self.defeated[1],self.defeatedColor,tolerance=15):
                        print("Exiting match")
                        self.lock.acquire()
                        self.state = Detectstate.EXIT
                        self.lock.release()
                except:
                    pass
                        
            elif self.state == Detectstate.PLAY:
                # click the play button
                sleep(0.05)
                py.click(x = self.playButton[0], y = self.playButton[1],button="left")
                sleep(0.05)
                self.lock.acquire()
                self.state = Detectstate.IDLE
                self.lock.release()
            
            elif self.state == Detectstate.LOAD:
                sleep(0.1)
                self.lock.acquire()
                self.state = Detectstate.IDLE
                self.lock.release()
            
            elif self.state == Detectstate.EXIT:
                # release right click
                py.mouseUp(button = Constants.movement_key)
                sleep(5)
                # click the exit button
                py.click(x = self.exitButton[0], y = self.exitButton[1],button="left")
                sleep(0.05)
                self.lock.acquire()
                self.state = Detectstate.IDLE
                self.lock.release()
