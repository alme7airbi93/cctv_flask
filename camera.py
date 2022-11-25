import cv2

import database


def gen_frames(cam_id):
    cameras = database.CCTV_DB().get_CCTV_List()
    for cam in cameras:
        if int(cam.doc_id) == int(cam_id):
            cctv = cam
            cap = cv2.VideoCapture(
                f'{cctv["protocol"]}://{cctv["username"]}:{cctv["password"]}@{cctv["ip"]}:{cctv["port"]}')

            while True:
                success, frame = cap.read()  # read the camera frame
                print("Success : "+ str(success) + " _" +  str(cctv["ip"]) )
                if not success:
                    break
                else:
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return "Camera not found"


