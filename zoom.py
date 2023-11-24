from windowcapture import WindowCapture
from constants import Constants
from time import sleep
from PIL import ImageGrab
import numpy as np
def subtract_tuple(tup1,tup2):
        return tuple(np.subtract(tup1, tup2))

def add_tuple(tup1,tup2):
    return tuple(map(sum, zip(tup1, tup2)))

wincap = WindowCapture(Constants.window_name)
wincap.set_window()
# add a delay for the screenshot
sleep(0.25)
# take a screenshot
screenshot_region = (wincap.offset_x,wincap.offset_y,
                        wincap.w+wincap.offset_x,
                        wincap.h+wincap.offset_y)

screenshot =  ImageGrab.grab(screenshot_region)

midpoint = (int(wincap.w/2), int(wincap.h/2))
max_width = int(0.2*wincap.w)
max_height = int(0.5*wincap.h)

topleft = subtract_tuple(midpoint,(max_width/2,max_height/2))
bottomright = add_tuple(midpoint,(max_width/2,max_height/2))
screenshot_cropped = screenshot.crop(topleft+bottomright)
zoom_size = 2
screenshot_cropped_resize = screenshot_cropped.resize((zoom_size*max_width,zoom_size*max_height))


for w in range(0,max_width):
    for h in range(0,max_height):
        # Get the RGB value
        RGB = screenshot_cropped.getpixel((w,h))
        if RGB == (72, 227, 53):
            print("True")
            break

screenshot_cropped_resize.show()