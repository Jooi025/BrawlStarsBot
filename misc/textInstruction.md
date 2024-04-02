### Importing game control
[How to import game control](https://github.com/Jooi025/BrawlStarsBot/blob/main/control/control.md)
### Testing and changing values
**Important - please disable Bluestacks' ads and close the left sidebar for the bot to work as intended**
1. Run "detection_test.py" to check if object detection is working
2. Change the brawler_name  in "constants.py" to your selected Brawler's name and run "constant.py".
3. If the brawler's stats in not found manually change the speed, attack range and height scale factor located below brawler_name at "constant.py" to the brawler's [speed and range](https://pixelcrux.com/Brawl_Stars/Brawlers/)  and to find the height scale factor run "hsf_finder". Also modify sharpCorner (True if the map has many walls, otherwise False) and centerOrder ( True if brawler spawns in the middle of the map, otherwise False).

4. Run "main.py"

5. Select solo showdown and "start bot" (enter 1)
