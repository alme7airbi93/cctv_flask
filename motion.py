import cv2
import numpy as np
from config import cfg
#---------------------------------------------------------------------------------------------------------------
# This function allows us to create a descending sorted list of contour areas., used in 'motionDetection' below
def contour_area(contours):
    cnt_area = []  # create an empty list
    for i in range(0,len(contours),1): # loop through all the contours
        # for each contour, use OpenCV to calculate the area of the contour
        cnt_area.append(cv2.contourArea(contours[i]))

    # Sort our list of contour areas in descending order
    list.sort(cnt_area, reverse=True)
    return cnt_area
#---------------------------------------------------------------------------------------------------
def show_windows(title, image):
    if cfg.video.Flag:
        cv2.imshow(title, image)
        key=cv2.waitKey(1) & 0xFF
        if key==ord('q'):
            cv2.destroyWindow(title)
            cfg.video.Flag = not (cfg.video.Flag)
#---------------------------------------------------------------------------------------------------
# import cascade file for recognition
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
import imutils
import numpy as np

conf = dict({   # developmental work
    "show_video":   cfg.video.Show,
    "delta_thresh": cfg.motion.senseThreshold,   # defaul 6
    "min_area":     cfg.motion.senseArea   # default = 600
})

def motionDetection(avg, fr):
    
    #frame = np.array(fr)
    frame = fr.copy()
    # convert the frame to grayscale, and blur it
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # if the average frame is None, initialize it
    if avg is None:
        print("[INFO] starting background model...")
        avg = gray.copy().astype("float")

    # accumulate the weighted average between the current frame and previous frames,
    # then compute the difference between the current frame and running average
    cv2.accumulateWeighted(gray, avg, 0.6)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
    thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=3)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:15]

    img = frame
    mot = 0
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if (cv2.contourArea(c) < conf["min_area"]):
            continue
        # compute the bounding box for the contour, draw it on the frame
        #print(frameDelta.shape)
        (x, y, w, h) = cv2.boundingRect(c)
        #if (x>350 and (x+w)<580 and y>50 and (y+h)<110):
        if (x>cfg.motion.maskLeft and (x+w)<cfg.motion.maskRight and y>cfg.motion.maskUp and (y+h)<cfg.motion.maskDwon):
            continue
        #else:
            #print(x,y,x+w, y+h)
        if cfg.motion.redBox:
            img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        if cfg.motion.blueBox:
            rect = cv2.minAreaRect(c)   # get the min area rect
            box  = cv2.boxPoints(rect)
            box  = np.int0(box)          # convert all coordinates floating point values to int
            img = cv2.drawContours(img, [box], 0, (255, 0, 0),1)  # draw a blue 'nghien' rectangle
        
            #print(cv2.contourArea(c),w,h)
        mot += 1

    if conf["show_video"]:
        # display the security feed
        cv2.imshow("Security Feed", img)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            exit(0)
    
    return img, mot, avg
#------------------------------------------------------------------------------------------------------------------------------------