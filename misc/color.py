import pyautogui 
from time import sleep
from windowcapture import WindowCapture
import keyboard

find_colour = False
wincap = WindowCapture("Bluestacks App Player")
windowSize = (wincap.w, wincap.h)
print(windowSize)

if find_colour:
    print("Press enter to get scale factor and RGB value\n")
    count = 0
    while 1:
        if keyboard.is_pressed('enter'):
            x,y = pyautogui.position()
            print(count)
            print("xScaleFactor: ",round(x/wincap.w,4))
            print("yScaleFactor: ",round(y/wincap.w,4))
            print("RGB: ",pyautogui.pixel(x,y))
            print("")
            count+=1
            sleep(0.5)
else:
    while True:
        defeated = (round(wincap.w*0.9782), round(wincap.h*0.1991))
        color = (62,0,0)
        print(pyautogui.pixelMatchesColor(defeated[0],defeated[1],color,tolerance=10))
        sleep(0.1)
        


                