import pyautogui 
from time import sleep
from windowcapture import WindowCapture
import keyboard

wincap = WindowCapture('Bluestacks App Player')
windowSize = (wincap.w, wincap.h)

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

                