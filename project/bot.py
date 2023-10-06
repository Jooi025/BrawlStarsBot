import cv2 as cv
from time import time,sleep
from threading import Thread, Lock
from math import *
import pyautogui
import numpy as np
import random
class BotState:
    INITIALIZING = 0
    # stating the bot
    
    SEARCHING = 1
    # searching for bush to hide

    # will try to search for the closest bush without enemy presence 
    
    MOVING = 2
    # move to the selected bush
    # brawler's tile speed and tile distance is used to calculate the time it takes
    # will know when "player" is stuck on obstacle (using opencv to calculate the 
    # similarity of previous screenshot and the current screenshot )
    
    #if enemy or storm is near the path it will try to search for another bush
    HIDING = 3
    # when "player" is inside the bush 
    
    # RELOCATE = 4
    # #if there is a storm or enemy close by
    
    # ATTACK = 5
    # # if enemy is close
    # # attack depends on brawler range (short,medium,long) 
    # # and distance to enemy (in tiles)

class Brawlbot:
    # tile constant
    tile_w = 26.75
    tile_h = 18.61
    border = 22

    sharpCorner = False
    centerOrder = True
    
    timeFactor = 1
    if sharpCorner:
        # time to move increase by 5% if maps have sharps corner
        timeFactor = 1.05

    MOVEMENT_STOPPED_THRESHOLD = 0.95
    HIDINGTIME = 10
    IGNORE_RADIUS = 0.5
    movement_screenshot = None
    screenshot = None
    INITIALIZING_SECONDS = 9
    results = []
    bushResult = []
    counter = 0

    def __init__(self,windowSize,speed,range) -> None:
        self.lock = Lock()
        # "brawler" chracteristic
        self.speed = speed
        self.range = range # 0:short, 1:medium , 2:long
        

        self.timestamp = time()
        self.window_w = windowSize[0]
        self.window_h = windowSize[1]
        self.centre_window = (self.window_w / 2, int((self.window_h / 2)+ self.border))

        # tile size of the game
        # depended on the dimension of the game
        self.tileSize = round((round(self.window_w/self.tile_w)+round(self.window_h/self.tile_h))/2)
        self.state = BotState.INITIALIZING
    
    def targets_ordered_by_distance(self, results, pos):
        # our character is always in the center of the screen
        # if player position in result is empty 
        # assume that player is in the middle of the screen
        if not(results[0]) or self.centerOrder :
            player_pos = (self.window_w / 2, int((self.window_h / 2)+ self.border))
        else:
            player_pos = results[0][0]
        # searched "python order points by distance from point"
        # simply uses the pythagorean theorem
        # https://stackoverflow.com/a/30636138/4655368
        def tile_distance(pos):
            return sqrt(((pos[0] - player_pos[0])/(self.window_w/self.tile_w))**2 + ((pos[1] - player_pos[1])/(self.window_h/self.tile_h))**2)
        # list of bush location is the in index 1 of results
        sortedResults = results[pos]
        sortedResults.sort(key=tile_distance)
        return sortedResults
    
    #return sqrt(((pos[0] - player_pos[0])/(self.window_w/self.tile_w))**2 + ((pos[1] - player_pos[1])/(self.window_h/self.tile_h))**2) 
    #return (sqrt((pos[0] - player_pos[0])**2 + (pos[1] - player_pos[1])**2)/self.tileSize)
    def tile_distance(self,player_pos,pos):
        return sqrt(((pos[0] - player_pos[0])/(self.window_w/self.tile_w))**2 + ((pos[1] - player_pos[1])/(self.window_h/self.tile_h))**2)
    
    def find_bush(self):
        if self.results:
            self.bushResult = self.targets_ordered_by_distance(self.results,1)
        if self.bushResult:
            return True
        else:
            return False
    
    def storm_direction(self):
        #p0 (self.centre_window) is coordinate of the middle of the screen
        #p1 is the coordinate of the player
        if self.results[0]:
            p0 = self.centre_window
            p1 = self.results[0][0]
            xDiff , yDiff = tuple(np.subtract(p0, p1))
            xBorder = self.window_w/20
            yBorder = self.window_h/20
            x = ""
            y =  ""
            #xDiff is positve
            if xDiff>xBorder:
                x = "d"
            elif xDiff<-xBorder:
                x = "a"
            if yDiff>yBorder:
                y = "s"
            elif yDiff<-yBorder:
                y = "w"
            if [x,y] == ["",""]:
                return []
            else:
                return [x,y]
    def bot_move(self):
        #get the nearest bush to the player
        if self.bushResult:
            x,y = self.bushResult[0]
            if not(self.results[0]) or self.centerOrder:
                player_pos = (self.window_w / 2, int((self.window_h / 2)+ self.border))
            else:
                player_pos = self.results[0][0]
            tileDistance = self.tile_distance(player_pos,(x,y))
            pyautogui.mouseDown(button='right',x = x, y = y)
            moveTime = tileDistance/self.speed
            moveTime = moveTime * self.timeFactor
            return moveTime
    
    def random_movement(self):
        if self.storm_direction():
            move_keys = self.storm_direction()
        else:
            move_keys = ["w", "a", "s", "d"]
        random_move = random.choice(move_keys)
        with pyautogui.hold(random_move):
            sleep(1)

    def random_movement_attack(self):
        if self.storm_direction():
            move_keys = self.storm_direction()
        else:
            move_keys = ["w", "a", "s", "d"]
        random_move = random.choice(move_keys)
        with pyautogui.hold(random_move):
            self.attack()
            sleep(0.5)
            self.attack()
            sleep(0.5)

    def is_enemy_in_range(self):
        """ 
        return boolen, notified bot if enemy is close to player
        """
        if self.results[0]:
            player_pos = self.results[0][0]
        # if player position in result is empty 
        # assume that player is in the middle of the screen
        else:
            player_pos = (self.window_w / 2, int((self.window_h / 2)+ self.border))

        if self.results[2]:
            enemyResults = self.targets_ordered_by_distance(self.results,2)
            self.enemyResults = [e for e in enemyResults if self.tile_distance(player_pos,e) > self.IGNORE_RADIUS]
            if self.enemyResults:
                enemyDistance = self.tile_distance(player_pos,self.enemyResults[0])
                if self.range == 0:
                    attackRange = 3 
                elif self.range == 1:
                    attackRange = 5
                elif self.range == 2:
                    attackRange = 9
                if enemyDistance < attackRange:
                    return True
                else:
                    return False
        
    def attack(self):
        if self.counter%4 == 0:
            # activate "gadget"
            pyautogui.press("f")
            sleep(0.01)
        # activate "super"
        pyautogui.press("e")
        sleep(0.01)
        pyautogui.press("space")

    def update_results(self,results):
        self.lock.acquire()
        self.results = results
        self.lock.release()

    def have_stopped_moving(self):  
        # if we haven't stored a screenshot to compare to, do that first
        if self.movement_screenshot is None:
            self.movement_screenshot = self.screenshot.copy()
            return False

        # compare the old screenshot to the new screenshot
        result = cv.matchTemplate(self.screenshot, self.movement_screenshot, cv.TM_CCOEFF_NORMED)
        # we only care about the value when the two screenshots are laid perfectly over one 
        # another, so the needle position is (0, 0). since both images are the same size, this
        # should be the only result that exists anyway
        similarity = result[0][0]
        print('Movement detection similarity: {}'.format(similarity))

        if similarity >= self.MOVEMENT_STOPPED_THRESHOLD:
            # pictures look similar, so we've probably stopped moving
            print('Movement detected stop')
            return True

        # looks like we're still moving.
        # use this new screenshot to compare to the next one
        self.movement_screenshot = self.screenshot.copy()
        return False
    

    def update_screenshot(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            if self.state == BotState.INITIALIZING:
                # do no bot actions until the startup waiting period is complete
                if time() > self.timestamp + self.INITIALIZING_SECONDS:
                    # start searching when the waiting period is over
                    self.lock.acquire()
                    self.state = BotState.SEARCHING
                    self.lock.release()
                else:
                    sleep(0.01)
            elif self.state == BotState.SEARCHING:
                sleep(0.01)
                success = self.find_bush()
                #if bush is detected
                if success:
                    self.lock.acquire()
                    self.timestamp = time()
                    self.state = BotState.MOVING
                    self.lock.release()
                #bus is not detected
                if (not success) and (self.counter%4 == 0):
                    print("Cannot find bush")
                    self.random_movement()
                    self.counter+=1
                
            elif self.state == BotState.MOVING:
                # time for player to move to the selected bush 
                moveTime = self.bot_move()
                # when player is moving check if player is stuck 
                if time() < self.timestamp + moveTime:
                    print("Moving to bush")
                    if not self.have_stopped_moving():
                        # wait a short time to allow for the character position to change
                        sleep(0.05)
                    #if player is stuck
                    else:
                        # cancel moving 
                        pyautogui.mouseUp(button = "right")
                        self.random_movement()
                        self.lock.acquire()
                        # and search for bush again
                        self.state = BotState.SEARCHING
                        self.lock.release()

                    if not(self.is_enemy_in_range()):
                        #added delay so the bot thread wont be faster than the main script
                        sleep(0.01)
                    #enemy is in range
                    else:
                        sleep(0.01)
                        print("Attacking enemy")
                        self.attack()
                # player successfully travel to the selected bush 
                else:
                    pyautogui.mouseUp(button = "right")
                    self.lock.acquire()
                    # change state to hiding
                    print("Hiding")
                    self.state = BotState.HIDING
                    self.timestamp = time()
                    self.lock.release()
                    
            elif self.state == BotState.HIDING:
                if time() < self.timestamp + self.HIDINGTIME:
                    #enemy is not in range 
                    if not(self.is_enemy_in_range()):
                        #added delay so the bot thread wont be faster than the main script
                        sleep(0.01)
                    #enemy is in range
                    else:
                        sleep(0.01)
                        print("Attacking enemy")
                        self.random_movement_attack()
                        
                else:
                    print("Changing state to search")
                    self.lock.acquire()
                    self.state = BotState.SEARCHING
                    self.lock.release()
            