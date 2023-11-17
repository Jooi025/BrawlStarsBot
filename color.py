import pyautogui
from time import sleep
from windowcapture import WindowCapture
import keyboard

find_colour = True
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
    loadColor = (224,22,22)
    w = windowSize[0]
    h = windowSize[1]
    left = wincap.border_pixels
    top = wincap.titlebar_pixels
    defeated = (round(w*0.9758)+left, round(h*0.2017)+top)
    playButton = (round(w*0.5984)+left,round(h*0.9159)+top)
    exitButton = (round(w*0.5059)+left,round(h* 0.9216)+top)
    loadButton = (round(w*0.0215+left),round(h*0.0583)+top)
    while True:
        
        defeated = (round(wincap.w*0.9782), round(wincap.h*0.1991))
        color = (62,0,0)
        print(pyautogui.pixelMatchesColor(defeated[0],defeated[1],color,tolerance=10))
        sleep(0.1)
        

