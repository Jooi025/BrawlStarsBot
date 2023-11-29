# BrawlStarsBot
Brawl stars bot for farming mastery through solo showdown. The bot will find bushes and hide, it also attacks enemies if they are within range. Macro is integrated into the code to automate when defeated, it will queue up for another match automatically. 

⚠️ **DISCLAIMER!!**  ****You can lose trophies while using the bot!!**** ⚠️  The bot's goal is to farm mastery.

## Info
Inspired by [OpenCV Object Detection in Games Python Tutorial playlist by "Learn Code By Gaming"](https://www.youtube.com/watch?v=KecMlLUuiE4&list=PL1m2M8LQlzfKtkKq2lK5xko4X-8EZzFPI) and ["How To Train YOLOv5 For Recognizing Game Objects In Real-Time" by "Jes Fink-Jensen"](https://betterprogramming.pub/how-to-train-yolov5-for-recognizing-custom-game-objects-in-real-time-9d78369928a8).

The Bluestacks app player is used to emulate Brawl Stars onto the computer. Bluestacks default game control is modified. The bot works well with tanky brawlers and on maps with little obstacles (wall, bush, fence, etc) and a lot of bush.
A recommended map to run the bot on is island invasion, using short/medium range and tanky brawlers such as Frank, Sam, Buster, Pearl, Nita, etc.

## Bot features
- Fully automated
   - When the player is defeated it will exit the match
   - Requeue another match
   - Start the bot when loading in
- Find the closest bush and hide in it 
- Attack the enemy when they are in the range
- Activate gadget when the enemy is closer to the player

  
****Demo of the bot:****
[![Watch the video](https://github.com/Jooi025/BrawlStarsBot/blob/main/misc/image/youtube_thumbnail.jpg)](https://youtu.be/TWmNfkQBVYk?si=CXaSBoAV-YknJPLt)

## Requirement
* Windows OS
* [Bluestacks 5](https://www.bluestacks.com/download.html) to run brawl star
* Python>= 3.8.0 installed (I used version 3.11.6)
## Some common errors
- If Brawl Stars is stuck on the loading screen, return to Bluestacks' home screen, hold down left click on the Brawl Stars' icon and select "App Info". Click "force stop" and select "Storage" and click "Clear cache". Now, try to open Brawl Stars again.
- After starting bot in main.py, the terminal displays "Play" multiple times, and the mouse doesn't move and click Play in the Brawl Stars' main menu. Close Pycharm or your IDE, and reopen it with administration permission. 

## How to install and run the bot?
Full video tutorial coming soon...
### 1. Clone Repo
1. Clone the repository 
```
git clone https://github.com/Jooi025/BrawlStarsBot.git
```
2. Install the required library
```
cd BrawlStarsBot
pip install -r requirements.txt
```
### 2. Importing game control
[How to import game control](https://github.com/Jooi025/BrawlStarsBot/blob/main/control.md)
### 3. Testing and changing values
1. Run "detection_test.py" to check if object detection is working
2. Change the brawler_name  in "constants.py" to your selected Brawler's name and run "constant.py".
3. If the brawler's stats in not found manually change the speed, attack range and height scale factor located below brawler_name at "constant.py" to the brawler's [speed and range](https://pixelcrux.com/Brawl_Stars/Brawlers/)  and to find the height scale factor run "hsf_finder". Also modify sharpCorner (True if the map has many walls, otherwise False) and centerOrder ( True if brawler spawns in the middle of the map, otherwise False).
     
4. Run "main.py"

5. Select solo showdown and "start bot" (enter 1)

 ## Improvement to be made
 - [ ] bot can attack power cube boxes and collect them
 - [x] improve detection of enemy (less false detect)
 - [ ] change player detection
 - [x] improve storm direction function 
 - [x] improve the screen detection of "defeated"
 - [x] fix spam printing of "stop bot" 
 - [x] improve fps for lower performance computer 



