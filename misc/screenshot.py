# import win32gui, win32ui, win32con,win32com.client
# import numpy as np
# import cv2 as cv

# def get_crop_screenshot(x1,y1,x2,y2):

#     # for now we will set hwnd to None to capture the primary monitor
#     hwnd = None

#     # get the window image data
#     wDC = win32gui.GetWindowDC(hwnd)
#     dcObj = win32ui.CreateDCFromHandle(wDC)
#     cDC = dcObj.CreateCompatibleDC()
#     dataBitMap = win32ui.CreateBitmap()
#     dataBitMap.CreateCompatibleBitmap(dcObj, x2, y2)
#     cDC.SelectObject(dataBitMap)
#     cDC.BitBlt((0, 0), (x2, y2), dcObj, (x1, y1), win32con.SRCCOPY)

#     # convert the raw data into a format opencv can read
#     signedIntsArray = dataBitMap.GetBitmapBits(True)
#     img = np.fromstring(signedIntsArray, dtype='uint8')
#     img.shape = (y2, x2, 4)

#     # free resources
#     dcObj.DeleteDC()
#     cDC.DeleteDC()
#     win32gui.ReleaseDC(hwnd, wDC)
#     win32gui.DeleteObject(dataBitMap.GetHandle())

#     # drop the alpha channel to work with cv.matchTemplate()
#     img = img[...,:3]

#     # make image C_CONTIGUOUS to avoid errors with cv.rectangle()
#     img = np.ascontiguousarray(img)

#     return img

# while(True):
#     screenshot = get_crop_screenshot(0,0,1000,500)
#     lower_red = np.array([0, 0, 0], dtype = "uint8")
#     upper_red= np.array([0,0,255], dtype = "uint8")
#     mask = cv.inRange(screenshot, lower_red, upper_red)
#     screenshot = cv.bitwise_and(screenshot, screenshot, mask = mask)
#     cv.imshow('Computer Vision', screenshot)

#     # press 'q' with the output window focused to exit.
#     # waits 1 ms every loop to process key presses
#     if cv.waitKey(1) == ord('q'):
#         cv.destroyAllWindows()
#         break

import pyautogui as py

py.moveTo(539,510)