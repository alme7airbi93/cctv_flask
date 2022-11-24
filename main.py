from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
from cctv_database import CCTV_DB

app = Flask(__name__, static_folder="static", template_folder="templates")
database = {'CCTV': CCTV_DB()}
cameras = []


def gen_frames(cam_id):
    global cameras

    for cam in cameras:
        if int(cam.doc_id) == int(cam_id):
            cctv = cam
            cap = cv2.VideoCapture(
                f'{cctv["protocol"]}://{cctv["username"]}:{cctv["password"]}@{cctv["ip"]}:{cctv["port"]}')

            while True:
                success, frame = cap.read()  # read the camera frame
                if not success:
                    break
                else:
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return "Camera not found"


@app.route("/")
def home():
    global cameras
    cameras = database['CCTV'].get_CCTV_List()
    return render_template("index.html", cameras=cameras)


@app.route("/addCamera", methods=['POST'])
def addCamera():
    global database

    validated = False
    try:
        camera = {
            'ip': request.form['ip'],
            'port': request.form['port'],
            'username': request.form['username'],
            'password': request.form['password'],
            'protocol': request.form['protocol']
        }
        ## Update validation
        validated = True
        if validated:
            database['CCTV'].save_CCTV(camera)
    except:
        print("Error addCamera")
    return redirect(url_for('home'))


@app.route("/deleteCamera/<id>", methods=['GET'])
def deleteCamera(id):
    global database
    database['CCTV'].delete_CCTV(id)
    return redirect(url_for('home'))


@app.route('/video_feed/<id>', methods=['GET', 'POST'])
def video_feed(id):
    return Response(gen_frames(id), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)
