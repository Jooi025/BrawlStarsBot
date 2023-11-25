# BrawlStarsBot
Brawl stars bot for farming mastery through solo showdown. The bot will find bushes and hide, it also attacks enemies if they are within range. Macro is integrated into the code to automate when defeated, it will queue up for another match automatically. 

⚠️ **DISCLAIMER!!**  ****You can lose trophies while using the bot!!**** ⚠️  The bot's goal is to farm mastery.

## Info
Inspired by [OpenCV Object Detection in Games Python Tutorial playlist by "Learn Code By Gaming"](https://www.youtube.com/watch?v=KecMlLUuiE4&list=PL1m2M8LQlzfKtkKq2lK5xko4X-8EZzFPI) and ["How To Train YOLOv5 For Recognizing Game Objects In Real-Time" by "Jes Fink-Jensen"](https://betterprogramming.pub/how-to-train-yolov5-for-recognizing-custom-game-objects-in-real-time-9d78369928a8).

The Bluestacks app player is used to emulate Brawl Stars onto the computer. Bluestacks default game control is modified. The bot works well with tanky brawlers and on maps with little obstacles (wall, bush, fence, etc) and a lot of bush.
A recommended map to run the bot on is island invasion, using short/medium range and tanky brawlers such as Frank, Sam, Buster, Pearl, Nita, etc.

****Demo of the bot:****
[![Watch the video](https://github.com/Jooi025/BrawlStarsBot/blob/main/misc/image/youtube_thumbnail.jpg)](https://youtu.be/TWmNfkQBVYk?si=CXaSBoAV-YknJPLt)

## Requirement
* Windows OS
* [Bluestacks 5](https://www.bluestacks.com/download.html) to run brawl star
* Python>= 3.8.0 installed

## How to install and run the bot?
Full video tutorial coming soon...
### Clone Repo
1. Clone the repository and install the required library
```
git clone https://github.com/Jooi025/BrawlStarsBot.git
cd BrawlStarsBot
pip install -r requirements.txt
```
### Importing game control
The game control scheme (com.supercell.brawlstars.cfg) as shown can be found at the [control folder](https://github.com/Jooi025/BrawlStarsBot/tree/main/control)

2. Open Bluestacks and select game control on the side panel, as shown below.

![alt text](https://github.com/Jooi025/BrawlStarsBot/blob/main/misc/image/game_control.jpg)

3. Select the controls editor, as shown below

![alt text](https://github.com/Jooi025/BrawlStarsBot/blob/main/misc/image/control_editor.jpg)

4. Select import at the top right corner, as shown below

![alt text](https://github.com/Jooi025/BrawlStarsBot/blob/main/misc/image/import.jpg)

5. Go to where you have installed the repository and select the control folder

![alt text](https://github.com/Jooi025/BrawlStarsBot/blob/main/misc/image/control.jpg)

6. Select "com.supercell.brawlstars.cfg" and import it

![alt text](https://github.com/Jooi025/BrawlStarsBot/blob/main/misc/image/importing.jpg)

7. Select "BOT" and import schemes

![alt text](https://github.com/Jooi025/BrawlStarsBot/blob/main/misc/image/bot_importing.jpg)

8. Select "BOT" and save, as shown below

![alt text](https://github.com/Jooi025/BrawlStarsBot/blob/main/misc/image/select_bot.jpg)

![alt text](https://github.com/Jooi025/BrawlStarsBot/blob/main/misc/image/save.jpg)

9. Exit control editor

   ![alt text](https://github.com/Jooi025/BrawlStarsBot/blob/main/misc/image/exiting.jpg)


10. Move and resize the movement joystick as shown and ****select the locked movement control****

![Alt text](control/controlSetup.jpg?raw=true "Example of gamecontrol in Bluestacks")

11. After finishing importing and modifying the control, collapse/close the side panel by pressing the top right button as shown below.  

![Alt text](https://github.com/Jooi025/BrawlStarsBot/blob/main/misc/image/side_panel_bluestacks.jpg )
### Testing and changing values
 12. Run "detection_test.py" to check if object detection is working
 13. Change the speed, attack range and height scale factor in "contants.py" to the brawler's [speed and range](https://pixelcrux.com/Brawl_Stars/Brawlers/)  and to find the height scale factor run "hsf_finder". Also modify sharpCorner (True if the map has many walls, otherwise False) and centerOrder ( True if brawler spawns in the middle of the map, otherwise False).
     
 14. Run "main.py"
 15. Select solo showdown and "start bot" (enter 1)

 ## Improvement to be made
 - [ ] bot can attack power cube boxes and collect them
 - [x] improve detection of enemy (less false detect)
 - [ ] change player detection
 - [x] improve storm direction function 
 - [x] improve the screen detection of "defeated"
 - [x] fix spam printing of "stop bot" 
 - [ ] improve fps for lower performance computer 



