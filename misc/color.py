import pyautogui
from time import sleep
from modules.windowcapture import WindowCapture
import keyboard

find_colour = 1
wincap = WindowCapture("Bluestacks App Player")
windowSize = (wincap.w, wincap.h)

if find_colour:
    print("Press q to get scale factor and RGB value\n")
    count = 1
    while 1:
        if keyboard.is_pressed('q'):
            x,y = pyautogui.position()
            print(x,y)
            print(count)
            print("xScaleFactor: ",round((x-wincap.offset_x)/wincap.w,4))
            print("yScaleFactor: ",round((y-wincap.offset_y)/wincap.h,4))
            print("RGB: ",pyautogui.pixel(x,y))
            print("")
            count+=1
            sleep(0.5)
# testing
else:
    proceedColor = (35, 115, 255)
    defeatedColor = (62,0,0)
    playColor = (224, 186, 8)
    loadColor = (177, 239, 74)
    w = windowSize[0]
    h = windowSize[1]
    left = wincap.offset_x
    top = wincap.offset_y
    defeated = (round(w*0.9683)+left, round(h*0.1969)+top)
    playButton = (round(w*0.5903)+left,round(h*0.9197)+top)
    exitButton = (round(w*0.493)+left,round(h*0.9187)+top)
    loadButton = (round(w*0.084)+left,round(h*0.1319)+top)
    proceedButton = (round(w*0.8093)+left, round(h*0.9165)+top)

    starDrop1 = (round(w*0.488)+left, round(h*0.9303)+top)
    starDrop2 = (round(w*0.5228)+left, round(h*0.9296)+top)
    starDropColor = (222, 72, 227)

    connection_lost_color = (66, 66, 66)
    connection_lost_cord = (round(w*0.4912)+left,round(h*0.5525)+top)
    reload_button = (round(w*0.2824)+left,round(h*0.5812)+top)
    count = 0
    while True:
        if pyautogui.pixelMatchesColor(playButton[0], playButton[1],playColor,tolerance=15):
            print("Play again ")
        elif pyautogui.pixelMatchesColor(loadButton[0], loadButton[1],loadColor,tolerance=25):
            print("Load in")
        elif pyautogui.pixelMatchesColor(defeated[0], defeated[1],defeatedColor,tolerance=15):
            print("Exit")
        # elif pyautogui.pixelMatchesColor(connection_lost_cord[0],connection_lost_cord[1],connection_lost_color,tolerance=1  ):
        #     print("Connection Lost")

        elif (pyautogui.pixelMatchesColor(starDrop1[0], starDrop1[1],starDropColor,tolerance=15) 
              or pyautogui.pixelMatchesColor(starDrop2[0], starDrop2[1],starDropColor,tolerance=15)):
            print(f"{count}: Star Drop")
            count += 1


        elif pyautogui.pixelMatchesColor(proceedButton[0], proceedButton[1],proceedColor,tolerance=15):
            print("Proceed")
        if keyboard.is_pressed("q"):
            pyautogui.moveTo(exitButton[0],exitButton[1])
        
        elif keyboard.is_pressed("l"):
            pyautogui.moveTo(reload_button[0],reload_button[1])

        elif keyboard.is_pressed("c"):
            pyautogui.moveTo(connection_lost_cord[0],connection_lost_cord[1])
        

