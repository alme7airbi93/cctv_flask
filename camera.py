import cv2
import time
import database
from datetime import datetime


def gen_frames(cam_id):
    cameras = database.CCTV_DB().get_CCTV_List()
    settings = database.SETTINGS_DB().get_settings_Dict()
    storagePath = str(settings['filePath']+'\\')
    start_time = time.time()
    for cam in cameras:
        if int(cam.doc_id) == int(cam_id):


            cctv = cam
            cap = cv2.VideoCapture(
                f'{cctv["protocol"]}://{cctv["username"]}:{cctv["password"]}@{cctv["ip"]}:{cctv["port"]}')


            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))
            fileName = storagePath + str(datetime.now().strftime("%Y-%m-%d%H%M%S")) + ".avi"
            out = cv2.VideoWriter(fileName, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10,
                                  (frame_width, frame_height))

            while True:
                now = time.time()
                success, frame = cap.read()  # read the camera frame
                elapsed = round(now - start_time)
                # print("Success : "+ str(success) + " _" +  str(cctv["ip"]) + " " + fileName)
                if not success:
                    break
                else:

                    if elapsed < int(settings['vidDuration']) * 60:
                        out.write(frame)
                    else:
                        out.release()
                        fileName = storagePath + str(datetime.now().strftime("%Y-%m-%d%H%M%S")) + ".avi"
                        out = cv2.VideoWriter(fileName, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10,(frame_width, frame_height))
                        print("Success : " + str(success) + " _" + str(cctv["ip"]) + " :::::::  " + fileName)
                        start_time = time.time()

                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return "Camera not found"


