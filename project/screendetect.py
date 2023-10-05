import pyautogui
from threading import Thread, Lock
from time import sleep
class Detectstate:
    IDLE = 0
    DETECT = 1
    EXIT = 2
    PLAY = 3
    LOAD = 4 
class Screendetect:
    defeatedColor = (62,0,0)      
    playColor = (224, 186, 8)
    loadColor = (224,22,22)
    def __init__(self,windowSize) -> None:
        self.state = Detectstate.DETECT
        self.lock = Lock()
        self.w = windowSize[0]
        self.h = windowSize[1]
        self.defeated = (round(self.w*0.9782), round(self.h*0.1991))
        self.playButton = (round(self.w*0.5929),round(self.h*0.9574))
        self.exitButton = (round(self.w*0.4969),round(self.h*0.96))
        self.loadButton = (round(self.w*0.02347),round(self.h*0.1199))
    
    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
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
                try:
                    if pyautogui.pixelMatchesColor(self.playButton[0], self.playButton[1],self.playColor,tolerance=15):
                        print("Play again ")
                        self.lock.acquire()
                        self.state = Detectstate.PLAY
                        self.lock.release()
                    elif pyautogui.pixelMatchesColor(self.loadButton[0], self.loadButton[1],self.loadColor,tolerance=15):
                        print("Load in")
                        self.lock.acquire()
                        sleep(3)
                        self.state = Detectstate.LOAD
                        self.lock.release()
                    elif pyautogui.pixelMatchesColor(self.defeated[0], self.defeated[1],self.defeatedColor,tolerance=15):
                        print("Exit")
                        self.lock.acquire()
                        self.state = Detectstate.EXIT
                        print("change state to exit")
                        self.lock.release()
                except:
                    pass

            elif self.state == Detectstate.PLAY:
                sleep(0.05)
                pyautogui.click(x = self.playButton[0], y = self.playButton[1],button="left")
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
                pyautogui.mouseUp(button = "right")
                sleep(5)
                pyautogui.click(x = self.exitButton[0], y = self.exitButton[1],button="left")
                sleep(0.05)
                self.lock.acquire()
                self.state = Detectstate.IDLE
                self.lock.release()





        