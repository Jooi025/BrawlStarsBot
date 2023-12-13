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

CONNECTION: When the connection is lost

PLAY: When the main menu of brawl stars
"""
class Detectstate:
    IDLE = 0
    DETECT = 1
    EXIT = 2
    PLAY_AGAIN = 3
    LOAD = 4
    CONNECTION = 5
    PLAY = 6
    PROCEED = 7 
    
class Screendetect:
    #RGB value
    defeatedColor = (62,0,0)
    playColor = (224, 186, 8)
    loadColor = (177, 239, 74)
    defeated_xScale = 0.9677
    defeated_yScale = 0.2285
    proceedColor = (35, 115, 255)
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
        self.defeated1 = (round(self.w*0.9656)+self.offset_x, round(self.h*0.152)+self.offset_y)
        self.defeated2 = (round(self.w*0.993)+self.offset_x, round(self.h*0.2046)+self.offset_y)
        self.playAgainButton = (round(self.w*0.5903)+self.offset_x, round(self.h*0.9197)+self.offset_y)
        self.playButton = (round(self.w*0.9419)+self.offset_x, round(self.h*0.8949)+self.offset_y)
        self.exitButton = (round(self.w*0.493)+self.offset_x, round(self.h*0.9187)+self.offset_y)
        self.loadButton = (round(self.w*0.084)+self.offset_x, round(self.h*0.1319)+self.offset_y)
        self.proceedButton = (round(self.w*0.8093)+self.offset_x, round(self.h*0.9165)+self.offset_y)
        self.connection_lost_color = (66, 66, 66)
        self.connection_lost_cord = (round(self.w*0.4912)+self.offset_x,round(self.h*0.5525)+self.offset_y)
        self.reload_button = (round(self.w*0.2824)+self.offset_x,round(self.h*0.5812)+self.offset_y)
        
    def start(self):
        """
        start screendetect
        """
        self.stopped = False
        t = Thread(target=self.run)
        t.setDaemon(True)
        t.start()

    def stop(self):
        """
        stop screendetect
        """
        self.stopped = True

    def run(self):
        while not self.stopped:
            sleep(0.01)
            if self.state == Detectstate.IDLE:
                sleep(3)
                self.state = Detectstate.DETECT
            
            elif self.state == Detectstate.DETECT:
                try:
                    if pyautogui.pixelMatchesColor(self.playAgainButton[0], self.playAgainButton[1],self.playColor,tolerance=15):
                        print("Playing again")
                        self.lock.acquire()
                        self.state = Detectstate.PLAY_AGAIN
                        self.lock.release()
                    elif pyautogui.pixelMatchesColor(self.loadButton[0], self.loadButton[1],self.loadColor,tolerance=30):
                        print("Loading in")
                        self.lock.acquire()
                        sleep(3)
                        self.state = Detectstate.LOAD
                        self.lock.release()
                    elif (pyautogui.pixelMatchesColor(self.defeated1[0], self.defeated1[1],
                                                     self.defeatedColor,tolerance=15)
                        or pyautogui.pixelMatchesColor(self.defeated2[0], self.defeated2[1],
                                                     self.defeatedColor,tolerance=15)):
                        print("Exiting match")
                        self.lock.acquire()
                        self.state = Detectstate.EXIT
                        self.lock.release()
                    # elif pyautogui.pixelMatchesColor(self.connection_lost_cord[0],self.connection_lost_cord[1],self.connection_lost_color,tolerance=1):
                    #     print("Connection Lost")
                    #     self.lock.acquire()
                    #     self.state = Detectstate.CONNECTION
                    #     self.lock.release()
                    elif pyautogui.pixelMatchesColor(self.playButton[0], self.playButton[1],self.playColor,tolerance=15):
                        print("Play")
                        self.lock.acquire()
                        self.state = Detectstate.PLAY
                        self.lock.release()
                    elif pyautogui.pixelMatchesColor(self.proceedButton[0], self.proceedButton[1],self.proceedColor,tolerance=15):
                        print("Proceed")
                        self.lock.acquire()
                        self.state = Detectstate.PROCEED
                        self.lock.release()
                
                except OSError:
                    pass
                        
            elif self.state == Detectstate.PLAY_AGAIN:
                # click the play button
                sleep(0.05)
                py.click(x = self.playAgainButton[0], y = self.playAgainButton[1],button="left")
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
                # release movement key
                py.mouseUp(button = Constants.movement_key)
                sleep(5)
                # click the exit button
                py.click(x = self.exitButton[0], y = self.exitButton[1],button="left")
                sleep(0.05)
                self.lock.acquire()
                self.state = Detectstate.IDLE
                self.lock.release()
            
            elif self.state == Detectstate.CONNECTION:
                sleep(20)
                py.click(x = self.reload_button[0], y = self.reload_button[1],button="left")
                sleep(0.05)
                self.lock.acquire()
                self.state = Detectstate.IDLE
                self.lock.release()
            
            elif self.state == Detectstate.PLAY:
                # click the play button
                sleep(0.05)
                py.click(x = self.playButton[0], y = self.playButton[1],button="left")
                sleep(0.05)
                self.lock.acquire()
                self.state = Detectstate.IDLE
                self.lock.release()
            elif self.state == Detectstate.PROCEED:
                sleep(0.5)
                py.click(x = self.proceedButton[0], y = self.proceedButton[1],button="left")
                sleep(6)
                print("playagain")
                py.click(x = self.playAgainButton[0], y = self.playAgainButton[1],button="left")
                sleep(0.5)
                self.lock.acquire()
                self.state = Detectstate.IDLE
                self.lock.release()