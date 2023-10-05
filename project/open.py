import math
import cv2 as cv
import pyautogui
def find_mid_point(x1,y1,x2,y2):
    return x1+int((x2-x1)/2),y1+int((y2-y1)/2)
def find_midpoint(x1,y1,x2,y2):
    return [(x1+int((x2-x1)/2),y1+int((y2-y1)/2))]
def tile_size(w,h):
    #tile constant
    tile_w = 25
    tile_h = 18
    avg=(round(w/tile_w)+round(h/tile_h))/2
    return round(avg)

def distance(x1,y1,x2,y2):
    distance = math.sqrt( ((x1-x2)**2)+((y1-y2)**2) )
    return distance

def draw(screenshot,results,classes):
    bgr = (0, 0,255)
    if results:
        # for cord in results[0]:
        #     cv.drawMarker(screenshot, cord , bgr ,thickness=2,markerType= cv.MARKER_CROSS,
        #                     line_type=cv.LINE_AA, markerSize=50) 
        #     cv.putText(screenshot, classes[0], cord, cv.FONT_HERSHEY_SIMPLEX, 0.7, bgr, 2)
        # for cord in results[1]:
        #     cv.drawMarker(screenshot, cord , bgr ,thickness=2,markerType= cv.MARKER_CROSS,
        #                     line_type=cv.LINE_AA, markerSize=50) 
        #     cv.putText(screenshot, classes[1], cord, cv.FONT_HERSHEY_SIMPLEX, 0.7, bgr, 2)
        # for cord in results[2]:
        #     cv.drawMarker(screenshot, cord , bgr ,thickness=2,markerType= cv.MARKER_CROSS,
        #                     line_type=cv.LINE_AA, markerSize=50) 
        #     cv.putText(screenshot, classes[2], cord, cv.FONT_HERSHEY_SIMPLEX, 0.7, bgr, 2)
        # for cord in results[3]:
        #     cv.drawMarker(screenshot, cord , bgr ,thickness=2,markerType= cv.MARKER_CROSS,
        #                     line_type=cv.LINE_AA, markerSize=50) 
        #     cv.putText(screenshot, classes[3], cord, cv.FONT_HERSHEY_SIMPLEX, 0.7, bgr, 2)

        for i in range(len(results)):
                #if the list is not empty
                if results[i]:
                    for cord in results[i]:
                        cv.drawMarker(screenshot, cord , bgr ,thickness=2,markerType= cv.MARKER_CROSS,
                                    line_type=cv.LINE_AA, markerSize=50) 
                        cv.putText(screenshot, classes[i], cord, cv.FONT_HERSHEY_SIMPLEX, 0.7, bgr, 2)
    return screenshot

def restart_macro():
    pyautogui.keyDown("ctrl")
    pyautogui.press("p")
    pyautogui.keyUp("ctrl")