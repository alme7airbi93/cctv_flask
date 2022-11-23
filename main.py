from flask import Flask, render_template, Response, request
import cv2

app = Flask(__name__, static_folder="static", template_folder="templates")

cctv_list = [{'id': 1,
              'ip': '192.168.50.231',
              'username': 'admin',
              'password': 'P@$$w0rd',
              'port': '554',
              'protocol': 'rtsp'}, {'id': 2,
                                    'ip': '192.168.50.230',
                                    'username': 'admin',
                                    'password': 'P@$$w0rd',
                                    'port': '554',
                                    'protocol': 'rtsp'},
             {'id': 3,
              'ip': '192.168.50.232',
              'username': 'admin',
              'password': 'P@$$w0rd',
              'port': '554',
              'protocol': 'rtsp'}
             ]


def gen_frames(id):
    cctv = {}

    for cam in cctv_list:
        if int(cam['id']) == int(id):
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
def hello():
    return render_template("index.html")


@app.route('/video_feed/<id>', methods=['GET', 'POST'])
def video_feed(id):
    return Response(gen_frames(id), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)
