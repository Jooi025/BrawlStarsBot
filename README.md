# BrawlStarsBot
⚠️ **DISCLAIMER!!**  ****You can lose trophies while using the bot!! The bot's goal is to farm mastery****  ⚠️

Brawl stars bot for farming mastery through solo showdown. The bot will find bushes and hide, it also attacks enemies if they are within range. Macro is integrated into the code to automate when defeated, it will queue up for another match automatically. 

## Info
Inspired by [OpenCV Object Detection in Games Python Tutorial playlist by "Learn Code By Gaming"](https://www.youtube.com/watch?v=KecMlLUuiE4&list=PL1m2M8LQlzfKtkKq2lK5xko4X-8EZzFPI) and ["How To Train YOLOv5 For Recognizing Game Objects In Real-Time" by "Jes Fink-Jensen"](https://betterprogramming.pub/how-to-train-yolov5-for-recognizing-custom-game-objects-in-real-time-9d78369928a8).

The Bluestacks app player is used to emulate Brawl Stars onto the computer and a custom Bluestacks control is used for the bot. The bot works well with tanky brawlers and on maps with little obstacles (wall, bush, fence, etc) and a lot of bush.
A recommended map to run the bot on is island invasion, using short/medium range and tanky brawlers such as Frank, Sam, Buster, Pearl, Nita, etc...

## Bot features
- Fully automated
   - When the player is defeated, it will exit the match
   - Requeue another match
   - Start the bot when loading in
- Find the closest bush and hide in it 
- Attack the enemy when they are in the range
- Activate gadget when the enemy is closer to the player
- Custom Bluestack game control for the bot

  
## Demo of the bot
[![Watch the video](https://github.com/Jooi025/BrawlStarsBot/blob/main/misc/image/youtube_thumbnail.jpg)](https://youtu.be/TWmNfkQBVYk?si=CXaSBoAV-YknJPLt)

## Requirement
* Windows OS
* [Bluestacks 5](https://www.bluestacks.com/download.html) to run Brawl Star and for custom control
* Python version 3.11.6

## How to install and run the bot?
### [Watch the tutorial and common error fix playlist](https://youtube.com/playlist?list=PLD9X_geub8rmkcpJSWzvoqmB9VZk-9TfO&si=7vrCV9s1kLviRaTL)
### Clone Repo
1. Clone the repository 
```
git clone https://github.com/Jooi025/BrawlStarsBot.git
```
2. Install the required library
```
cd BrawlStarsBot
pip install -r requirements.txt
```
[Writing instruction](https://github.com/Jooi025/BrawlStarsBot/blob/main/misc/textInstruction.md)
### Update Repo 
```
cd BrawlStarsBot
git pull
```
 ## Improvement to be made
 - [ ] bot can attack power cube boxes and collect them
 - [x] improve detection of enemy (less false detect)
 - [ ] change player detection and don't need to measure HSF 
 - [x] improve storm direction function 
 - [x] improve the screen detection of "defeated"
 - [x] fix spam printing of "stop bot" 
 - [x] improve fps for lower performance computer 



