import cv2
import time
import database
from datetime import datetime
import os


def gen_frames(cam_id):
    cameras = database.CCTV_DB().get_CCTV_List()
    settings = database.SETTINGS_DB().get_settings_Dict()
    storagePath = str(settings['filePath'] + '\\')
    start_time = time.time()

    for cctv in cameras:
        if int(cctv.doc_id) == int(cam_id):
            cap = cv2.VideoCapture(f'{cctv["protocol"]}://{cctv["username"]}:{cctv["password"]}@{cctv["ip"]}:{cctv["port"]}')
            print("Started  @  : " + str(datetime.now().strftime("%Y-%m-%d-%H%M%S")))

            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))
            fileName = storagePath + "\\" + str(cctv.doc_id) + "\\" + str(
                datetime.now().strftime("%Y-%m-%d-%H%M%S")) + ".avi"
            if not os.path.isdir(storagePath + "\\" + str(cctv.doc_id)):
                os.makedirs(storagePath + "\\" + str(cctv.doc_id))
            out = cv2.VideoWriter(fileName, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10,
                                  (frame_width, frame_height))
            recordDuration = int(settings['vidDuration']) * 60
            print("Record Duration : " + str(recordDuration))
            while True:
                now = time.time()
                success, frame = cap.read()  # read the camera frame
                elapsed = round(now - start_time)

                if not success:
                    cap.release()
                    cap = cv2.VideoCapture(f'{cctv["protocol"]}://{cctv["username"]}:{cctv["password"]}@{cctv["ip"]}:{cctv["port"]}')
                    print("Stopped @  : " + str(datetime.now().strftime("%Y-%m-%d-%H%M%S")))
                else:
                    try:
                        if elapsed < recordDuration:
                            out.write(frame)
                            # time.sleep(0.25)
                        else:
                            out.release()
                            print("Record Saved : " + fileName)
                            print("Starting new ...")
                            fileName = storagePath + "\\" + str(cctv.doc_id) + "\\" + str(
                                datetime.now().strftime("%Y-%m-%d-%H%M%S")) + ".avi"
                            out = cv2.VideoWriter(fileName, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10,
                                                  (frame_width, frame_height))
                            start_time = time.time()

                    except Exception as e:
                        print("Error Rised : "+ str(e))

                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return "Camera not found"
