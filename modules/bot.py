from time import time,sleep
from threading import Thread, Lock
from math import *
from collections import deque
import pyautogui as py
import numpy as np
from constants import Constants
"""
INITIALIZING: Initialize the bot
SEARCHING: Find the next objective based on mode profile (bush, cube box, enemy)
MOVING: Move to the selected objective
HIDING: Stop movement and hide in the bush (solo-focused profiles)
ATTACKING: Player will attack and activate gadget when enemy is nearby

"""
class BotState:
    INITIALIZING = 0
    SEARCHING = 1
    MOVING = 2
    HIDING = 3
    ATTACKING = 4

class Brawlbot:
    # In game tile width and height ratio with respect aspect ratio
    tile_w = 24
    tile_h = 17
    midpoint_offset = Constants.midpoint_offset

    # Map with sharp corners
    sharpCorner = Constants.sharpCorner
    # Either go to the closest bush to the player or the center
    centerOrder = Constants.centerOrder
    IGNORE_RADIUS = 0.5
    movement_screenshot = None
    screenshot = None
    INITIALIZING_SECONDS = 2
    results = []
    bushResult = []
    counter = 0
    direction = ["top","bottom","right","left"]
    current_bush = None
    last_player_pos = None
    last_closest_enemy = None
    border_size = 1
    stopped = True
    topleft = None
    avg_fps = 0
    enemy_move_key = None
    timeFactor = 1
    
    # time to move increase by 5% if maps have sharps corner
    if sharpCorner: timeFactor = 1.05

    def __init__(self,windowSize,offsets,speed,attack_range) -> None:
        self.lock = Lock()
        self.class_index = {name: i for i, name in enumerate(Constants.classes)}
        self.player_index = self.class_index.get("Player")
        self.bush_index = self.class_index.get("Bush")
        self.enemy_index = self.class_index.get("Enemy")
        self.cubebox_index = self.class_index.get("Cubebox")
        self.teammate_index = self.class_index.get("Teammate")
        self.game_mode = Constants.active_game_mode
        self.mode_profile = Constants.selected_game_mode
        self.team_mode = self.game_mode in ("team_3v3", "team_5v5")
        self.centerOrder = self.mode_profile["centerOrder"]
        self.enemy_prediction_seconds = self.mode_profile["prediction_seconds"]
        self.aggression = self.mode_profile["aggression"]
        self.hide_in_bush = self.mode_profile["hide_in_bush"]
        self.teammate_support_range = self.mode_profile["teammate_support_range"]
        self.team_aggression_distance_multiplier = self.mode_profile["team_aggression_distance_multiplier"]
        self.search_priority = self.mode_profile.get("search_priority", ["Bush", "Cubebox", "Enemy"])
        self.objective_move_cap_seconds = self.mode_profile.get("objective_move_cap_seconds")
        self.rank_push_enabled = Constants.rank_push_enabled
        self.current_rank = Constants.current_rank
        self.target_rank = Constants.target_rank
        self.enemy_history = deque(maxlen=2)
        # Deterministic fallback order reduces erratic movement and makes behavior reproducible.
        self.fallback_directions = ("w", "a", "s", "d")
        self.fallback_index = 0
        self.last_attack_time = 0
        self.last_gadget_time = 0
        self.last_enemy_seen_timestamp = None
        self.attack_cooldown_seconds = 0.25
        self.gadget_cooldown_seconds = 2.0
        self.enemy_lost_grace_seconds = 0.45
        if self.rank_push_enabled:
            print(f"Rank push enabled: current={self.current_rank}, target={self.target_rank}")

        # "brawler" chracteristic
        self.speed = speed
        # short range
        if attack_range >0 and attack_range <=4:
            range_multiplier = 1
            hide_multiplier = 1.3
        # medium range
        elif attack_range > 4 and attack_range <=7:
            range_multiplier = 0.85
            hide_multiplier = 1
        # long range
        elif attack_range > 7:
            range_multiplier = 0.8
            hide_multiplier = 0.8
        
        # attack range in tiles
        self.alert_range = attack_range + 2
        self.attack_range = range_multiplier*attack_range
        self.gadget_range = 0.9*self.attack_range
        self.hide_attack_range = 3.5 # visible to enemy in the bush
        self.HIDINGTIME = hide_multiplier * 23
        # Team modes require faster regrouping and less passive bush time.
        if self.team_mode:
            self.HIDINGTIME = min(self.HIDINGTIME, 6)
        
        self.timestamp = time()
        self.window_w = windowSize[0]
        self.window_h = windowSize[1]
        self.center_window = (self.window_w / 2, int((self.window_h / 2)+ self.midpoint_offset))

        # tile size of the game
        # depended on the dimension of the game
        self.tileSize = round((round(self.window_w/self.tile_w)+round(self.window_h/self.tile_h))/2)
        self.state = BotState.INITIALIZING
        
        # offset
        self.offset_x = offsets[0]
        self.offset_y = offsets[1]

    def _safe_results(self, index):
        if index is None or not self.results:
            return []
        if index < 0 or index >= len(self.results):
            return []
        return self.results[index]

    def _player_position(self):
        player_detections = self._safe_results(self.player_index)
        if player_detections:
            return player_detections[0]
        return self.center_window

    def _teammate_in_support_range(self):
        teammate_detections = self._safe_results(self.teammate_index)
        if not teammate_detections:
            return False
        player_pos = self._player_position()
        distances = [self.tile_distance(player_pos, teammate) for teammate in teammate_detections]
        if not distances:
            return False
        closest_teammate = min(distances)
        return closest_teammate <= self.teammate_support_range

    def _update_enemy_history(self, enemy_pos):
        now = time()
        self.enemy_history.append((now, enemy_pos))

    def _predict_enemy_position(self):
        if len(self.enemy_history) < 2:
            return None
        (t0, p0), (t1, p1) = self.enemy_history
        dt = t1 - t0
        if dt <= 0:
            return None
        vx = (p1[0] - p0[0]) / dt
        vy = (p1[1] - p0[1]) / dt
        predicted_x = p1[0] + vx * self.enemy_prediction_seconds
        predicted_y = p1[1] + vy * self.enemy_prediction_seconds
        return (predicted_x, predicted_y)

    def _next_fallback_direction(self):
        """
        Return the next fallback movement key using a deterministic direction cycle.
        """
        key = self.fallback_directions[self.fallback_index]
        self.fallback_index = (self.fallback_index + 1) % len(self.fallback_directions)
        return key

    def _normalize_move_key(self, move_keys):
        """
        Normalize movement input into a single key string.
        Accepts a single key or list of keys and falls back to a deterministic
        direction cycle when no valid key is available.
        """
        if isinstance(move_keys, str) and move_keys:
            if move_keys in self.fallback_directions:
                return move_keys
            return self._next_fallback_direction()
        if isinstance(move_keys, list):
            filtered = [key for key in move_keys if key in self.fallback_directions]
            if filtered:
                return filtered[0]
        return self._next_fallback_direction()

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the __init__ constructor.
    def get_screen_position(self, cordinate):
        """
        Apply bluestacks' window offset
        :param cordinate (tuple): cordinate in the cropped screenshot
        :return: cordinate with offset applied
        """
        return (cordinate[0] + self.offset_x, cordinate[1] + self.offset_y)
    
    # storm method
    def guess_storm_direction(self):
        """
        Predict in game storm direction through the player position.

        eg. if player is off centre to the right guess the storm direction
        to be on the right.

        :return: (List) list of x and y direction or list of empty string
        """
        # asign x and y direction
        x_direction = ""
        y_direction =  ""
        # if there is a detection
        if self.results:
            # there player detection
            player_detections = self._safe_results(self.player_index)
            if player_detections:
                x_border = (self.window_w/self.tile_w)*self.border_size
                y_border = (self.window_h/self.tile_h)*self.border_size
                # coordinate of the middle of the screen
                p0 = self.center_window
                # coordinate of the player
                p1 = player_detections[0]
                # get the difference between centre and the player
                xDiff , yDiff = tuple(np.subtract(p1, p0))
                # player is on the right
                if xDiff>x_border:
                    x_direction = self.direction[2]
                # player is on the left
                elif xDiff<-x_border:
                    x_direction = self.direction[3]
                # player is on the bottom
                if yDiff>y_border:
                    y_direction = self.direction[1]
                # player is on the top
                elif yDiff<-y_border:
                    y_direction = self.direction[0]
                return [x_direction,y_direction]
            else:
                return 2*[""]
        else:
            return 2*[""]
    
    def storm_movement_key(self):
        """
        get movement key to move away from the storm

        :return: (List) list of movement keys or an empty list
        """
        x = ""
        y = ""
        # if there is detection
        if self.results:
            # if there is player detection
            if self._safe_results(self.player_index):
                # predict the storm direction
                direction = self.guess_storm_direction()
                if direction[0] == self.direction[2]:
                    x = "a"
                # player is on the left
                elif direction[0] == self.direction[3]:
                    x = "d"
                # player is on the bottom
                if direction[1] == self.direction[1]:
                    y = "w"
                # player is on the top
                elif direction[1] == self.direction[0]:
                    y = "s"
        if [x,y] == ["",""]:
            return []
        else:
            return [x,y]

    def get_quadrant_bush(self):
        """
        get the quadrant to select a bush to move to.

        :return: False (boolean)
                 (List) list of "quadrants"
        """
        length = 0
        direction = self.guess_storm_direction()
        for i in range(len(direction)):
            if len(direction[i]) > 0:
                length += 1
                index = i
        if length == 0:
            return False
        elif length == 1:
            single_direction = direction[index]
            # top
            if single_direction == self.direction[0]:
                return [[0,3],[2,3]]
            # bottom
            elif single_direction == self.direction[1]:
                return [[0,3],[0,1]]
            # right
            elif single_direction == self.direction[2]:
                return [[0,1],[0,3]]
            # left
            elif single_direction == self.direction[3]:
                return [[2,3],[0,3]]
        elif length == 2:
            # top right
            if direction == [self.direction[0],self.direction[2]]:
                return [[0,2],[1,3]]
            # top left
            elif direction == [self.direction[0],self.direction[3]]:
                return [[1,3],[1,3]]
            # bottom right
            elif direction == [self.direction[1],self.direction[2]]:
                return [[0,2],[0,2]]
            # bottom left
            elif direction == [self.direction[1],self.direction[3]]:
                return [[1,3],[0,2]]
        
    # bush method
    def ordered_bush_by_distance(self, index):
        # our character is always in the center of the screen
        # if player position in result is empty
        # assume that player is in the middle of the screen
        if self.centerOrder:
            player_position = self.center_window
        else:
            player_position = self._player_position()
        def tile_distance(position):
            return sqrt(((position[0] - player_position[0])/(self.window_w/self.tile_w))**2 
                        + ((position[1] - player_position[1])/(self.window_h/self.tile_h))**2)
        # list of bush location is the in index 1 of results
        unfilteredResults = self._safe_results(index)
        filteredResult = []
        # get quadrant
        quadrant = self.get_quadrant_bush()
        if quadrant:
            x_scale = self.window_w/3
            y_scale = self.window_h/3
            for x,y in unfilteredResults:
                # find bushes in the quadrant
                if ((x > quadrant[0][0]*x_scale and x <= quadrant[0][1]*x_scale)
                    and (y > quadrant[1][0]*y_scale and y <= quadrant[1][1]*y_scale)):
                    filteredResult.append((x,y))
            filteredResult.sort(key=tile_distance)
            if filteredResult:
                return filteredResult
        # if quadrant is False or filteredResult is empty
        if not(quadrant) or not(filteredResult):
            unfilteredResults.sort(key=tile_distance)
            return unfilteredResults
    
    def ordered_results_by_distance(self, index):
        """
        Sort detections for any class by distance from the player.
        """
        player_position = self._player_position()
        def tile_distance(position):
            return sqrt(((position[0] - player_position[0])/(self.window_w/self.tile_w))**2
                        + ((position[1] - player_position[1])/(self.window_h/self.tile_h))**2)
        sorted_results = list(self._safe_results(index))
        sorted_results.sort(key=tile_distance)
        return sorted_results
        
    def tile_distance(self,player_position,position):
        """
        get the tile distance between two coordinate

        :param player_position(tuple): position of the player
        :param position(tuple): coordinate of some position
        """
        return sqrt(((position[0] - player_position[0])/(self.window_w/self.tile_w))**2 + ((position[1] - player_position[1])/(self.window_h/self.tile_h))**2)
    
    def find_bush(self):
        """
        sort the bush by distance and assigned it to self.bushResult
        :return: True or False (boolean)
        """
        if self.results:
            self.bushResult = self.ordered_bush_by_distance(self.bush_index)
        if self.bushResult:
            return True
        else:
            return False
        

    def move_to_bush(self):
        """
        find the moving time from the distance and the player's speed
        :return moveTime (float): The amount of time to move to the selected bush
        """
        if self.bushResult:
            # if len(self.bushResult) > 1:
            #     index = 1
            # else:
            #     index = 0
            x,y = self.bushResult[0]
            player_pos = self._player_position()
            tileDistance = self.tile_distance(player_pos,(x,y))
            x,y = self.get_screen_position((x,y))
            py.mouseDown(button=Constants.movement_key,x=x, y=y)
            moveTime = tileDistance/self.speed
            moveTime = moveTime * self.timeFactor
            print(f"Distance: {round(tileDistance,2)} tiles")
            return moveTime

    def move_to_target(self, target_position, max_move_time=None):
        """
        Move toward a target detection position.
        """
        if target_position is None:
            return None
        x, y = target_position
        player_pos = self._player_position()
        tileDistance = self.tile_distance(player_pos, (x, y))
        x, y = self.get_screen_position((x, y))
        py.mouseDown(button=Constants.movement_key, x=x, y=y)
        moveTime = (tileDistance / self.speed) * self.timeFactor
        if max_move_time is not None:
            moveTime = min(moveTime, max_move_time)
        print(f"Distance: {round(tileDistance,2)} tiles")
        return moveTime

    def acquire_objective(self):
        """
        Select a movement objective by profile priority.
        """
        for class_name in self.search_priority:
            class_index = self.class_index.get(class_name)
            if class_index is None:
                continue
            ordered = self.ordered_results_by_distance(class_index)
            if ordered:
                move_time = self.move_to_target(
                    ordered[0],
                    max_move_time=self.objective_move_cap_seconds
                )
                if move_time is not None:
                    return class_name, move_time
        return None, None
    
    # enemy and attack method
    def attack(self):
        """
        Press the attack key
        :return: True when an attack key press is executed, False when blocked by cooldown.
        """
        now = time()
        if now - self.last_attack_time < self.attack_cooldown_seconds:
            return False
        print("attacking enemy")
        attack_key = "e"
        py.press(attack_key)
        self.last_attack_time = now
        return True

    def gadget(self):
        """
        Press the gadget key
        :return: True when gadget key press is executed, False when blocked by cooldown.
        """
        now = time()
        if now - self.last_gadget_time < self.gadget_cooldown_seconds:
            return False
        print("activate gadget")
        gadget_key = "f"
        py.press(gadget_key)
        self.last_gadget_time = now
        return True

    def hold_movement_key(self,key,time):
        """
        Hold down a key for a certain amount time

        :param key (string): key to be hold
        :param time (float): time to hold the key
        """
        with py.hold(key):
            sleep(time)

    def storm_random_movement(self):
        """
        Get storm-escape movement keys and hold a deterministic fallback key for one second.
        """
        move_keys = self.storm_movement_key()
        move_key = self._normalize_move_key(move_keys)
        hold_time = 1
        self.hold_movement_key(move_key,hold_time)
    
    def stuck_random_movement(self):
        """
        Get unstuck movement keys and hold a deterministic fallback key for one second.
        """
        move_keys = self.get_movement_key(self.bush_index)
        move_key = self._normalize_move_key(move_keys)
        with py.hold(move_key):
            sleep(1)

    def get_movement_key(self,index):
        """
        get enemy direction
        :return:(List) List of x and y direction
        """
        # asign x and y direction
        x_key = ""
        y_key = ""
        if self.results:
            player_pos = self._player_position()
            if self._safe_results(index):
                # enemy index
                if index == self.enemy_index:
                    p0 = self.enemyResults[0]
                elif index == self.bush_index:
                    p0 = self.bushResult[0]
                p1 = player_pos
                xDiff , yDiff = tuple(np.subtract(p1, p0))
                # right
                if xDiff>0:
                    x_key = "d"
                # left
                elif xDiff<0:
                    x_key = "a"
                # bottom
                if yDiff>0:
                    y_key = "s"
                # top
                elif yDiff<0:
                    y_key = "w"
                return [x_key,y_key]
        return []
    
    def enemy_fallback_movement(self):
        """
        Move player away from the enemy and attack
        """
        if not(self.enemy_move_key):
            move_keys = self.get_movement_key(self.enemy_index)
            move_key = self._normalize_move_key(move_keys)
        else:
            move_key = self._normalize_move_key(self.enemy_move_key)
        with py.hold(move_key):
            py.press("e",presses=2,interval=0.4)

    def enemy_distance(self):
        """
        Calculate the enemy distance from the player
        """
        if self.results:
            # player coordinate
            player_pos = self._player_position()
            # enemy coordinate
            if self._safe_results(self.enemy_index):
                self.enemyResults = self.ordered_results_by_distance(self.enemy_index)
                if self.enemyResults:
                    closest_enemy = self.enemyResults[0]
                    self._update_enemy_history(closest_enemy)
                    self.last_enemy_seen_timestamp = time()
                    enemyDistance = self.tile_distance(player_pos, closest_enemy)
                    # print(f"Closest enemy: {round(enemyDistance,2)} tiles")
                    return enemyDistance
        return None
    
    def is_enemy_in_range(self):
        """
        Check if enemy is in range of the player
        :return (boolean): True or False
        """
        enemyDistance = self.enemy_distance()
        if enemyDistance:
            if self.team_mode and self._teammate_in_support_range():
                # Slightly increase aggression in team fights with nearby support.
                enemyDistance = enemyDistance * self.team_aggression_distance_multiplier
            predicted_enemy = self._predict_enemy_position()
            if predicted_enemy:
                predicted_distance = self.tile_distance(self._player_position(), predicted_enemy)
                # Prefer the closest threat estimate to avoid delayed reactions.
                enemyDistance = min(enemyDistance, predicted_distance)
            effective_attack_range = self.attack_range * self.aggression
            effective_gadget_range = self.gadget_range * self.aggression
            # ranges in tiles
            if (enemyDistance > effective_attack_range
                and enemyDistance <= self.alert_range):
                self.enemy_move_key = self.get_movement_key(self.enemy_index)
            elif (enemyDistance > effective_gadget_range 
                  and enemyDistance <= effective_attack_range):
                self.attack()
                return True
            elif enemyDistance <= effective_gadget_range:
                self.gadget()
                self.attack()
                return True
        return False

    def is_enemy_close(self):
        """
        Check if enemy is visible in the bush
        :return (boolean): True or False
        """
        enemyDistance = self.enemy_distance()
        if enemyDistance:
            if enemyDistance <= self.hide_attack_range:
                self.gadget()
                self.attack()
                return True
        return False

    def is_player_damaged(self):
        """
        Check if player is damaged
        :return (boolean): True or False
        """
        if self.topleft:
            width = abs(self.topleft[0] - self.bottomright[0])
            height = abs(self.topleft[1] - self.bottomright[1])
            w1 = int(self.topleft[0] + width/3)
            w2 = int(self.topleft[0] + 2*(width/3))
            h = int(self.topleft[1] - height/2)
            try:
                if (py.pixelMatchesColor(w1,h,(204, 34, 34),tolerance=20)
                    or py.pixelMatchesColor(w2,h,(204, 34, 34),tolerance=20)):
                    print(f"player is damaged")
                    return True
            except OSError:
                pass
        return False
    
    def have_stopped_moving(self):
        """
        Check if player have stop moving
        :return (boolean): True or False
        """
        if self.results:
            player_detections = self._safe_results(self.player_index)
            if player_detections:
                player_pos = player_detections[0]
                if self.last_player_pos is None:
                    self.last_player_pos = player_pos
                else:
                    # last player position is the same as the current
                    if self.last_player_pos == player_pos:
                        self.counter += 1
                        if self.counter == 2:
                            print("have stopped moving or stuck")
                            return True
                    else:
                        # reset counter
                        self.counter = 0
                    self.last_player_pos = player_pos
        return False

    def update_results(self,results):
        """
        update results from the detection
        """
        self.lock.acquire()
        self.results = results
        self.lock.release()
    
    def update_player(self,topleft,bottomright):
        """
        update player position for the is_player_damaged function
        """
        self.lock.acquire()
        self.topleft = topleft
        self.bottomright =bottomright
        self.lock.release()

    def update_screenshot(self, screenshot):
        """
        update screenshot
        """
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        """
        start the bot
        """
        self.stopped = False
        self.loop_time = time()
        self.count = 0
        t = Thread(target=self.run)
        t.setDaemon(True)
        t.start()

    def stop(self):
        """
        stop the bot
        """
        self.stopped = True
        # reset last player position
        self.last_player_pos = None

    def run(self):
        while not self.stopped:
            sleep(0.01)
            if self.state == BotState.INITIALIZING:
                # do no bot actions until the startup waiting period is complete
                if time() > self.timestamp + self.INITIALIZING_SECONDS:
                    # start searching when the waiting period is over
                    self.lock.acquire()
                    self.state = BotState.SEARCHING
                    self.lock.release()

            elif self.state == BotState.SEARCHING:
                if self.is_enemy_in_range():
                    self.lock.acquire()
                    self.state = BotState.ATTACKING
                    self.lock.release()
                    continue

                objective, move_time = self.acquire_objective()
                if objective and move_time is not None:
                    print(f"Moving to {objective.lower()}")
                    self.moveTime = move_time
                    self.lock.acquire()
                    self.timestamp = time()
                    self.state = BotState.MOVING
                    self.lock.release()
                else:
                    print("Cannot find objective")
                    self.storm_random_movement()

            elif self.state == BotState.MOVING:
                # when player is moving check if player is stuck
                if self.have_stopped_moving():
                    # cancel moving
                    py.mouseUp(button = Constants.movement_key)
                    self.stuck_random_movement()
                    # and search for bush again
                    self.lock.acquire()
                    self.state = BotState.SEARCHING
                    self.lock.release()
                #if player is stuck
                else:
                    sleep(0.15)

                if self.is_enemy_in_range():
                    self.lock.acquire()
                    self.state = BotState.ATTACKING
                    self.lock.release()
                # player successfully travel to the selected bush
                if time() > self.timestamp + self.moveTime:
                    py.mouseUp(button = Constants.movement_key)
                    self.lock.acquire()
                    self.timestamp = time()
                    if self.hide_in_bush:
                        print("Hiding")
                        self.state = BotState.HIDING
                    else:
                        print("Reposition complete")
                        self.state = BotState.SEARCHING
                    self.lock.release()
                    
            elif self.state == BotState.HIDING:
                if not self.hide_in_bush:
                    self.lock.acquire()
                    self.state = BotState.SEARCHING
                    self.lock.release()
                    continue
                if time() > self.timestamp + self.HIDINGTIME or self.is_player_damaged():
                    print("Changing state to search")
                    self.lock.acquire()
                    self.state = BotState.SEARCHING
                    self.lock.release()

                if self.centerOrder:
                    if self.is_enemy_close():
                        print("Enemy is nearby")
                        self.lock.acquire()
                        self.state = BotState.ATTACKING
                        self.lock.release()
                else:
                    if self.is_enemy_in_range():
                        print("Enemy in range")
                        self.lock.acquire()
                        self.state = BotState.ATTACKING
                        self.lock.release()
            elif self.state == BotState.ATTACKING:
                if self.is_enemy_in_range():
                    self.enemy_fallback_movement()
                else:
                    if (self.last_enemy_seen_timestamp is not None
                        and time() - self.last_enemy_seen_timestamp <= self.enemy_lost_grace_seconds):
                        self.enemy_fallback_movement()
                    else:
                        self.lock.acquire()
                        self.state = BotState.SEARCHING
                        self.lock.release()
                    
            self.fps = (1 / (time() - self.loop_time))
            self.loop_time = time()
            self.count += 1
            if self.count == 1:
                self.avg_fps = self.fps
            else:
                self.avg_fps = (self.avg_fps*self.count+self.fps)/(self.count + 1)
