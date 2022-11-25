from flask import Flask, render_template, Response, request, redirect, url_for
from camera import gen_frames
from database import CCTV_DB, SETTINGS_DB

app = Flask(__name__, static_folder="static", template_folder="templates")
database = {'CCTV': CCTV_DB(), 'SETTINGS': SETTINGS_DB(), }
cameras = []


@app.route("/")
def home():
    global cameras
    global settings
    cameras = database['CCTV'].get_CCTV_List()
    settings = database['SETTINGS'].get_settings_Dict()
    return render_template("index.html", cameras=cameras, settings=settings)


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


@app.route("/updateSettings", methods=['POST'])
def updateSettings():
    global database
    settings = {}
    for key, val in request.form.items():
        settings[key] = val

    if 'isRecording' in settings:
        settings['isRecording'] = True
    else:
        settings['isRecording'] = False

    validated = False
    try:
        storage = database['SETTINGS'].get_settings_Dict()

        # Update validation
        validated = True
        if len(storage) > 0:
            if validated:
                database['SETTINGS'].update_settings(settings)
        else:
            database['SETTINGS'].save_settings(settings)

    except Exception as e:
        print("Error updating settings : ", str(e))
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
