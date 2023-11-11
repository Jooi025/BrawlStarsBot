import cv2 as cv
from constants import Constants

def find_midpoint(x1,y1,x2,y2):
        #x2 > x1
        #y2 > y1
        return [(x1+int((x2-x1)/2),y1+int((y2-y1)/2))]

def detection(model,classes,screenshot,windowSize):
        brawler_height = Constants.heightScaleFactor * windowSize[1]
        thickness = 2
        #bgr
        red = (0, 0, 255) 
        # create empty nested list
        detection_cord= len(classes)*[[]]
        results = model(screenshot)
        labels, cord = results.xyxyn[0][:, -1].cpu().numpy(), results.xyxyn[0][:, :-1].cpu().numpy()
        n = len(labels)
        for i in range(n):
            # player class
            if labels[i] == 0:
                threshold = Constants.player_threshold
            # bush class
            elif labels[i] == 1:
                threshold = Constants.bush_threshold
            # enemy class
            elif labels[i] == 2:
                threshold = Constants.enemy_threshold
            # cube box class
            elif labels[i] == 3:
                threshold = Constants.cubebox_threshold
            row = cord[i]
            if row[4] >= threshold:
                x1, y1, x2, y2 = int(row[0] * windowSize[0]), int(row[1] * windowSize[1]), int(row[2] * windowSize[0]), int(row[3] * windowSize[1])
                midpoint = find_midpoint(x1,y1,x2,y2)
                if classes[int(labels[i])] == "Player":
                    midpoint =  [( midpoint[0][0], int(midpoint[0][1] + brawler_height))]
                if classes[int(labels[i])] == "Enemy":
                    #standardised enemy height and their label
                    height = y2 - y1
                    y1 = y1 + (height+0.2*windowSize[1])
                    midpoint = [( midpoint[0][0], int(midpoint[0][1] + 0.05*windowSize[1]))]
                detection_cord[int(labels[i])] = detection_cord[int(labels[i])] + midpoint  
                cv.drawMarker(screenshot, midpoint[0],
                                    red ,thickness=thickness,
                                    markerType= cv.MARKER_CROSS,
                                    line_type=cv.LINE_AA, markerSize=50) 
                cv.putText(screenshot, classes[int(labels[i])], 
                            midpoint[0], cv.FONT_HERSHEY_SIMPLEX, 0.7, red, 2)  
        return screenshot,detection_cord
                
def annotate(windowSize,screenshot,fps):
    border = 22
    xsplit = 27
    ysplit = 19
    xBorder = windowSize[0]/xsplit
    yBorder = windowSize[1]/ysplit
    x_scale = int(windowSize[0]/3)
    y_scale = int(windowSize[1]/3)
    color = (0,255,0)
    thickness = 2
    size = 3
    xTop = int(xBorder*((xsplit-size)/2))
    yTop = int(yBorder*((ysplit-size)/2))+border

    xBottom = int(xBorder*((xsplit+size)/2))
    yBottom = int(yBorder*((ysplit+size)/2))+border
    
    cv.rectangle(screenshot, (xTop, yTop), (xBottom, yBottom), (0,255,0), 2)
    cv.drawMarker(screenshot, (int(windowSize[0]/2),int((windowSize[1]/2)+22)),
                color ,thickness=thickness,markerType= cv.MARKER_CROSS,
                line_type=cv.LINE_AA, markerSize=50) 
    #quadrant line
    cv.line(screenshot,(x_scale,0),(x_scale,3*y_scale),color,thickness)
    cv.line(screenshot,(2*x_scale,0),(2*x_scale,3*y_scale),color,thickness)
    cv.line(screenshot,(0,y_scale),(3*x_scale,y_scale),color,thickness)
    cv.line(screenshot,(0,2*y_scale),(3*x_scale,2*y_scale),color,thickness)
    cv.putText(screenshot,f"FPS:{int(fps)}",(20,windowSize[1]-20),
            cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    
    # attack range
    # cv.circle(screenshot, (int(windowSize[0]/2,int((windowSize[1]/2)+22))), radius, color, thickness)
    return screenshot
