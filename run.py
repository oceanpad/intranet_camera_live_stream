#!/usr/bin/env python
from importlib import import_module
from flask import Flask, render_template, Response, redirect, url_for, request, flash
from camera_opencv import Camera
import time
import cv2
import os

app = Flask(__name__)
app.secret_key = 'a5b039e1-1d58-11e9-9ca1-7831c1d3560c'

def gen_ip_camera(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    camera = Camera()
    return Response(gen_ip_camera(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/live')
def live():
    return Response(gen_live(),mimetype='multipart/x-mixed-replace; boundary=frame')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/live/upload', methods=['POST'])
def live_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = 'live.jpg'
            file.save(os.path.join('static/stream/', filename))
            return "success"

def gen_live():
    frame = []
    while True:
        try:
            time.sleep(0.025)
            img = cv2.imread("static/stream/live.jpg")
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except Exception as err:
            print str(err)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False,  port=5000, threaded=True)
