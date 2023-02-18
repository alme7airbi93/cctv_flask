#! /usr/bin/env python
# coding=utf-8
# file_version v5 dated 17.feb.2023
# Author: tjmail

from easydict import EasyDict as edict
__C = edict(); cfg = __C
__C.video = edict(); __C.motion = edict()
##-------------------------------------------------------------------------------------------------------------------------##
# used to set video related parameters
__C.video.Fps     = 10       # default = 10, video saving FPS
__C.video.Encoder = 'WMV1'   # default = 'MJPG', 4-byte code used to specify the video codec
__C.video.Scale   = 1        # default value=1, This down-scales video frames in height, recommended 0.5 to 1.0
__C.video.Show    = False     # default False, set to True for developmental use

# used to set motion senstitivity parameters
__C.motion.senseThreshold = 4    # default = 6, The min threshold of frame-difference to be pervieved as motion.  
__C.motion.senseArea      = 100  # default = 900, The min Area threshold for detection

# Used to create mask on motion detection on video time stamp
__C.motion.maskLeft  = 350    # default = 350 Time stamp left (xmin-axis)
__C.motion.maskRight = 1880   # default = 580, Time stamp right (xmax-axis)  
__C.motion.maskUp    =  50    # default = 50, Time stamp upper (ymin-axis) 
__C.motion.maskDwon  = 310    # default 110,  Time stamp lower (ymax-axis)  

__C.motion.redBox  = True # to make red-box (square) visible  
__C.motion.blueBox = True # to make blue-box (rectangle/contoure) visible  

# settings for video encoder, can be replaced in line 15 above
#__C.video.Encoder = 'WMV2'   # default = 'MJPG', 4-byte code used to specify the video codec
#__C.video.Encoder = 'MJPG'   # default = 'MJPG', 4-byte code used to specify the video codec

# size comparisons on various video encoders
#>>> cv2.cv.FOURCC( *"XVID" )    1145656920   -- 3mb
#>>> cv2.cv.FOURCC( *"MJPG" )    1196444237   -- 6mb
#>>> cv2.cv.FOURCC( *"WMV1" )     827739479   -- 3m
#>>> cv2.cv.FOURCC( *"WMV2" )     844516695   -- 3mb