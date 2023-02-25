import cv2
import time
import database
from datetime import datetime
import os
from motion import motionDetection
from config import cfg

def gen_frames(cam_id):
    cameras = database.CCTV_DB().get_CCTV_List()
    settings = database.SETTINGS_DB().get_settings_Dict()
    storagePath = str(settings['filePath'])
    fourcc = cv2.VideoWriter_fourcc(*cfg.video.Encoder)
    start_time = time.time()
    frameCmp = None
    frameCount = 0 
    KPS = cfg.video.Fps # desired frame per second

    for cctv in cameras:
        
        if int(cctv.doc_id) == int(cam_id):
            cap = cv2.VideoCapture(f'{cctv["protocol"]}://{cctv["username"]}:{cctv["password"]}@{cctv["ip"]}:{cctv["port"]}')
            time.sleep(0.25)
            print("Started  @  : " + str(datetime.now().strftime("%Y-%m-%d-%H%M%S")))
            
            fps = round(cap.get(cv2.CAP_PROP_FPS))
            hop = round(fps / KPS)

            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))    #frame_width = int(cap.get(3))
            frame_height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))   #frame_height= int(cap.get(4))
            if frame_width <10 or frame_height < 10:  # for very less resolution video, generate warning.
                print('Camera Errro, exiting...', frame_width, frame_height)
                break
            
            dimensions = (int(frame_width * cfg.video.Scale), int(frame_height * cfg.video.Scale) )

            fileName = storagePath + "\\" + str(cctv.doc_id) + "\\" + str(datetime.now().strftime("%Y-%m-%d")) + "\\" + str(datetime.now().strftime("%Y-%m-%d-%H%M%S")) + ".avi"

            if not os.path.isdir(storagePath + "\\" + str(cctv.doc_id) + "\\" + str(datetime.now().strftime("%Y-%m-%d"))):
                os.makedirs(storagePath + "\\" + str(cctv.doc_id) + "\\" + str(datetime.now().strftime("%Y-%m-%d")))
            
            out = cv2.VideoWriter(fileName, fourcc, cfg.video.Fps, dimensions)

            recordDuration = int(settings['vidDuration']) * 60
            print("Record Duration : " + str(recordDuration))

            while cap.isOpened():   # chaanged fron True by TJ
                now = time.time()
                success, frame = cap.read()  # read the camera frame
                elapsed = round(now - start_time)
                
                if not success:
                    cap.release()
                    #Tries to reset !!
                    cap = cv2.VideoCapture(f'{cctv["protocol"]}://{cctv["username"]}:{cctv["password"]}@{cctv["ip"]}:{cctv["port"]}')
                    print("Stopped @  : " + str(datetime.now().strftime("%Y-%m-%d-%H%M%S")))
                
                else:
                    frameCount += 1
                    the_frame = frame.copy()
                    if cfg.video.Scale < 1.0:   # rescale if rescale factor is set (lower than 1)
                        the_frame = cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)  # rescaling using opencv
                                           
                    try:
                        if elapsed < recordDuration:
                            if frameCount % 5 == 0:  # detect motion every 5th frame
                                the_frame, motion, frameCmp = motionDetection(frameCmp, the_frame)  # call motion detection function
                            
                            if (cfg.video.Show):
                                print('motion detected:', motion >0)
                            
                            if frameCount % hop == 0:   # only write the selected frame
                                if motion > 0:
                                    out.write(the_frame) #TJ write after all the processing,
                        else:
                            out.release()
                            print("Record Saved : " + fileName, elapsed)
                            
                            print("Starting new ...")
                            fileName = storagePath + "\\" + str(cctv.doc_id) + "\\" + str(datetime.now().strftime("%Y-%m-%d")) + "\\" + str(datetime.now().strftime("%Y-%m-%d-%H%M%S")) + ".avi"
                            if not os.path.isdir(storagePath + "\\" + str(cctv.doc_id) + "\\" + str(
                                    datetime.now().strftime("%Y-%m-%d"))):
                                os.makedirs(storagePath + "\\" + str(cctv.doc_id) + "\\" + str(
                                    datetime.now().strftime("%Y-%m-%d")))

                            #initalizing file handle
                            out = cv2.VideoWriter(fileName, fourcc, cfg.video.Fps, dimensions)
                            #initializing timer                       
                            start_time = time.time()
                            frameCount = 0
                      
                    except Exception as e:
                        print("Error Rised : "+ str(e))

                    ret, buffer = cv2.imencode('.jpg', the_frame)   # the frame can be replaced with rescaled_frame if related to disk storage
                    vframe = buffer.tobytes()
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + vframe + b'\r\n')
    
    return "Camera not found"