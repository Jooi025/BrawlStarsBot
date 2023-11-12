# BrawlStarsBot
Brawl stars bot for farming mastery through solo showdown. Bot will find bushes and hide, its also attacks enemy if they are within the range. Macro is intergrated into the code to automate when defeated, it will queue up for another match. Noted that you could lose trophy while using the bot. However, if you pick the right brawler and on the right map you could gain trophies. Bot works well with name tag around four characters.

## Info
Inspired by [OpenCV Object Detection in Games Python Tutorial playlist by "Learn Code By Gaming"](https://www.youtube.com/watch?v=KecMlLUuiE4&list=PL1m2M8LQlzfKtkKq2lK5xko4X-8EZzFPI).
Used yolov5 for object detection, followed ["How To Train YOLOv5 For Recognizing Game Objects In Real-Time" by "Jes Fink-Jensen"](https://betterprogramming.pub/how-to-train-yolov5-for-recognizing-custom-game-objects-in-real-time-9d78369928a8) (might need to sign in to medium), tutorial for how to get started with yolov5.


****Demo of the bot:****

[![Watch the video](https://github.com/Jooi025/BrawlStarsBot/blob/main/misc/image/youtube_thumbnail.jpg)](https://www.youtube.com/watch?v=kp5izpAKA-Y)

Bluestacks app player is used to emulate brawl stars onto computer. Bluestacks default game control is modified. Bot works well with tanky brawlers and on maps with little obstacle (wall,bush,fence,etc) and lot of bush.
A recomended map to run the bot on is island invasion, using short/medium range and tanky brawlers such as Frank, Sam, Buster, Pearl, Nita, etc.

## Requirement
* [Bluestacks 5](https://www.bluestacks.com/download.html) to run brawl star
* Python>= 3.8.0 installed

## How to run the bot?
1. Clone repo and install the required library
```
git clone https://github.com/Jooi025/BrawlStarsBot.git
cd BrawlStarsBot
pip install -r requirements.txt
```
2. Import bluestacks game control and modify brawl stars control in training ground

Game control scheme (com.supercell.brawlstars.cfg) as shown can be found at the [bluestacks game control](https://github.com/Jooi025/BrawlStarsBot/tree/main/control), you would need to import com.supercell.brawlstars.cfg to the control editor of Bluestacks [(tutorial on how to import game control)](https://support.bluestacks.com/hc/en-us/articles/360056129291-How-to-import-your-game-controls-from-BlueStacks-4-and-use-them-in-BlueStacks-5). 

Modified game control :

![Alt text](control/controlSetup.jpg?raw=true "Example of gamecontrol in Bluestacks")

move and resize the movement joystick as showned and ****select the locked movement control****

 3. Run "detection_test.py" to check if object detection is working
 4. Change the speed and range in "Contants.py" to the brawler's speed and range
 5. Position bluestacks in the top left corner and run "main.py", as showned in the demo.
 6. Select "start bot" (enter 1) after loading in the match. **Do not start bot on the loading screen**

 ## Improvement to be made
 - [ ] bot can attack power cube boxes and collect them
 - [ ] improve detection on enemy (less false detect)
 - [ ] change player detection
 - [ ] improve storm direction function 
 - [ ] improve the screendetect of "defeated"
 - [ ] fix spam printing of "stop bot" 




