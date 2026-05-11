"""
The screendetect module uses pyautogui to matches pixels' color and take specific action depending on the matches.
e.g. play again button - When play again button is detect by pyautogui.pixelMatchesColor() it will click the play again button.
"""

import pyautogui as py
from threading import Thread, Lock
from time import sleep, time
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

PROCEED: When the match is finished, it will click the proceed button

STARDROP: Whenever there is a star drop in the main menu, it will collect the star drop
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
    STARDROP = 8
    
class Screendetect:
    #RGB value
    defeatedColor = (62,0,0)
    playColor = (224, 186, 8)
    loadColor = (0, 1, 0)
    proceedColor = (35, 115, 255)
    connection_lost_color = (66, 66, 66)
    starDropColor = (222, 72, 227)

    def __init__(self,windowSize,offset) -> None:
        """
        Constructor for the Screendectect class
        """
        self.state = Detectstate.DETECT
        self.lock = Lock()
        # Start safe by assuming the bot is stopped until main loop updates this flag.
        self.bot_stopped = True
        self.w = windowSize[0]
        self.h = windowSize[1]
        self.offset_x = offset[0]
        self.offset_y = offset[1]
        self.last_action_time = {}
        self.action_cooldowns = {
            Detectstate.PLAY_AGAIN: 1.0,
            Detectstate.LOAD: 1.0,
            Detectstate.EXIT: 2.0,
            Detectstate.PLAY: 1.0,
            Detectstate.PROCEED: 1.0,
            Detectstate.STARDROP: 5.0,
        }

        # Coordinate
        self.defeated1 = (round(self.w*0.9656)+self.offset_x, round(self.h*0.152)+self.offset_y)
        self.defeated2 = (round(self.w*0.993)+self.offset_x, round(self.h*0.2046)+self.offset_y)

        self.starDrop1 = (round(self.w*0.488)+ self.offset_x, round(self.h*0.9303) + self.offset_y)
        self.starDrop2 = (round(self.w*0.5228)+ self.offset_x, round(self.h*0.9296) + self.offset_y)

        self.playAgainButton = (round(self.w*0.5903)+self.offset_x, round(self.h*0.9197)+self.offset_y)
        self.playButton = (round(self.w*0.9419)+self.offset_x, round(self.h*0.8949)+self.offset_y)
        self.exitButton = (round(self.w*0.493)+self.offset_x, round(self.h*0.9187)+self.offset_y)
        self.loadButton = (round(self.w*0.8057)+self.offset_x, round(self.h*0.9675)+self.offset_y)
        self.proceedButton = (round(self.w*0.8093)+self.offset_x, round(self.h*0.9165)+self.offset_y)

        self.connection_lost_cord = (round(self.w*0.4912)+self.offset_x,round(self.h*0.5525)+self.offset_y)
        self.reload_button = (round(self.w*0.2824)+self.offset_x,round(self.h*0.5812)+self.offset_y)

    def update_bot_stop(self,bot_stopped):
        self.bot_stopped = bot_stopped

    def set_state(self, state):
        with self.lock:
            self.state = state

    def _state_ready(self, state):
        now = time()
        last = self.last_action_time.get(state, 0)
        cooldown = self.action_cooldowns.get(state, 0)
        if now - last < cooldown:
            return False
        self.last_action_time[state] = now
        return True

    def _pixel_match(self, coordinate, color, tolerance):
        try:
            return py.pixelMatchesColor(coordinate[0], coordinate[1], color, tolerance=tolerance)
        except OSError:
            return False
    
    def start(self):
        """
        start screendetect
        """
        self.stopped = False
        t = Thread(target=self.run, daemon=True)
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
                # Keep a short pause to avoid spam while remaining responsive to UI changes.
                sleep(0.5)
                self.state = Detectstate.DETECT
            
            elif self.state == Detectstate.DETECT:
                if self._pixel_match(self.playAgainButton, self.playColor, tolerance=15):
                    if self._state_ready(Detectstate.PLAY_AGAIN):
                        print("Playing again")
                        self.set_state(Detectstate.PLAY_AGAIN)

                elif self._pixel_match(self.loadButton, self.loadColor, tolerance=30):
                    if self._state_ready(Detectstate.LOAD):
                        print("Loading in")
                        self.set_state(Detectstate.LOAD)

                elif (self._pixel_match(self.defeated1, self.defeatedColor, tolerance=15)
                    or self._pixel_match(self.defeated2, self.defeatedColor, tolerance=15)) and not(self.bot_stopped):
                    if self._state_ready(Detectstate.EXIT):
                        print("Exiting match")
                        self.set_state(Detectstate.EXIT)

                elif (self._pixel_match(self.starDrop1, self.starDropColor, tolerance=15)
                    or self._pixel_match(self.starDrop2, self.starDropColor, tolerance=15)):
                    if self._state_ready(Detectstate.STARDROP):
                        print("Collecting Star Drop")
                        self.set_state(Detectstate.STARDROP)

                elif self._pixel_match(self.playButton, self.playColor, tolerance=15):
                    if self._state_ready(Detectstate.PLAY):
                        print("Play")
                        self.set_state(Detectstate.PLAY)

                elif self._pixel_match(self.proceedButton, self.proceedColor, tolerance=25):
                    if self._state_ready(Detectstate.PROCEED):
                        print("Proceed")
                        self.set_state(Detectstate.PROCEED)
                        
            elif self.state == Detectstate.PLAY_AGAIN:
                # click the play button
                sleep(0.05)
                py.click(x=self.playAgainButton[0], y=self.playAgainButton[1], button="left")
                sleep(0.05)
                self.set_state(Detectstate.IDLE)
            
            elif self.state == Detectstate.LOAD:
                sleep(0.1)
                self.set_state(Detectstate.IDLE)
            
            elif self.state == Detectstate.EXIT:
                # release movement key
                py.mouseUp(button = Constants.movement_key)
                sleep(5)
                # click the exit button
                py.click(x=self.exitButton[0], y=self.exitButton[1], button="left")
                sleep(0.05)
                self.set_state(Detectstate.IDLE)
            
            elif self.state == Detectstate.CONNECTION:
                sleep(20)
                py.click(x=self.reload_button[0], y=self.reload_button[1], button="left")
                sleep(0.05)
                self.set_state(Detectstate.IDLE)
            
            elif self.state == Detectstate.PLAY:
                # click the play button
                sleep(0.05)
                py.click(x=self.playButton[0], y=self.playButton[1], button="left")
                sleep(0.05)
                self.set_state(Detectstate.IDLE)
            
            elif self.state == Detectstate.PROCEED:
                sleep(0.5)
                py.click(x=self.proceedButton[0], y=self.proceedButton[1], button="left", clicks=2)
                sleep(0.5)
                self.set_state(Detectstate.IDLE)
            
            elif self.state == Detectstate.STARDROP:
                py.press("e",presses=5)
                sleep(6)
                py.press("e")
                self.set_state(Detectstate.IDLE)
