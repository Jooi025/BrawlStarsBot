import pyautogui
from time import sleep
from windowcapture import WindowCapture
import keyboard

find_colour = False
wincap = WindowCapture("Bluestacks App Player")
windowSize = (wincap.w, wincap.h)

if find_colour:
    print("Press q to get scale factor and RGB value\n")
    count = 1
    while 1:
        if keyboard.is_pressed('q'):
            x,y = pyautogui.position()
            print(count)
            print("xScaleFactor: ",round((x-wincap.border_pixels)/wincap.w,4))
            print("yScaleFactor: ",round((y-wincap.titlebar_pixels)/wincap.h,4))
            print("RGB: ",pyautogui.pixel(x,y))
            print("")
            count+=1
            sleep(0.5)
# testing
else:
    defeatedColor = (62,0,0)
    playColor = (224, 186, 8)
    loadColor = (187, 239, 74)
    w = windowSize[0]
    h = windowSize[1]
    left = wincap.offset_x
    top = wincap.offset_y
    defeated = (round(w*0.9683)+left, round(h*0.1969)+top)
    playButton = (round(w*0.5903)+left,round(h*0.9197)+top)
    exitButton = (round(w*0.493)+left,round(h*0.9187)+top)
    loadButton = (round(w*0.0855)+left,round(h*0.1306)+top)
    while True:
        if pyautogui.pixelMatchesColor(playButton[0], playButton[1],playColor,tolerance=15):
            print("Play again ")
        elif pyautogui.pixelMatchesColor(loadButton[0], loadButton[1],loadColor,tolerance=15):
            print("Load in")
        elif pyautogui.pixelMatchesColor(defeated[0], defeated[1],defeatedColor,tolerance=15):
            print("Exit")

        if keyboard.is_pressed("q"):
            pyautogui.moveTo(exitButton[0],exitButton[1])

        

